var twitterStream = {};
twitterStream.stream_open = false;
twitterStream.intervalId = undefined;
twitterStream.queryInterval = 1000 * 15;
twitterStream.tweets = [];
twitterStream.tweetFeatures = [];
twitterStream.tweetIndex = 0;
twitterStream.tweetLayer = undefined;
twitterStream.feature_id = 0;
twitterStream.bad_hashtags = [];


twitterStream.toggleStream = function(_button) {
    console.log("toggling stream...");

    if ( twitterStream.stream_url == undefined ||
        twitterStream.get_tweets_url == undefined ) {
            console.log("Error with ajax urls");
            return;
        }

    // Start leaflet GeoJson layer for Twitter
    if (twitterStream.tweetLayer == undefined) {
        twitterStream.tweetLayer = L.geoJson(false, {
            onEachFeature: function(feature, layer) {
                layer.bindPopup(feature.properties.popupContent);
            },
            filter: function(feature, layer) {
                return (feature.properties.lang === "en") &&
                    (feature.geometry !== null);
            },
            pointToLayer: function(feature, latlng) {
                var icon = L.icon({
                    iconSize: [32, 32],
                    iconAnchor: [13, 27],
                    iconUrl: 'http://png.findicons.com/files/icons/2823/turkuvaz_1/128/twitter.png'
                });

                return L.marker(latlng, {icon: icon});
            }
        }).addTo(aoi_feature_edit.map);
    }

    // if stream is active, close it
    if ( twitterStream.stream_open ) {
        console.log("closing stream...");
        twitterStream.$button.text("Start Stream");
        twitterStream.closeStream();
    } else {
        console.log("starting stream...");
        twitterStream.$button = _button;
        twitterStream.$button.text("Stop Stream");
        twitterStream.startStream();
    }

    //twitterStream.stream_open = !this.stream_open;
}

twitterStream.startStream = function() {
    var map = aoi_feature_edit.map;
    if (map && map.getBounds().isValid()) {
        var query_bounds = map.getBounds().toBBoxString();
        twitterStream.query_bounds = query_bounds;

        setTimeout( function() {
            twitterStream.intervalId = twitterStream.getTweets();
        }, 5000 );

        twitterStream.toggleStreamAjaxFunc();

        console.log("Stream Opened");

    } else {
        console.log("Invalid map or bounds!");
    }
}

twitterStream.toggleStreamAjaxFunc = function() {
    console.log("before stream_open", twitterStream.stream_open);
    jQuery.ajax({
        type: "GET",
        url: twitterStream.stream_url,
        data: {"bounds" : twitterStream.query_bounds, "client-stream" : twitterStream.stream_open},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(res) {
            if ( res.tweets != undefined ) {
                res.tweets = JSON.parse(res.tweets);
            }

            // Add tweets to map if tweets where returned
            if (res.tweets != undefined && res.tweets != null) {
                res.tweets = JSON.parse(res.tweets);

                if ( res.tweets instanceof Array && res.tweets.length > 0) {
                    twitterStream.tweets.push(res.tweets);
                    twitterStream.addTweetLayer();
                }
            }
            console.log(res);
            console.log("after stream_open", twitterStream.stream_open);
        },
        error: function(e, msg) {
            twitterStream.closeStream();
            console.log(e.status + " - " + e.statusText + " [" + msg + "]");
            console.log(e);
        }
    }); //ajax
}

twitterStream.closeStream = function() {
    clearInterval(twitterStream.intervalId);

    twitterStream.toggleStreamAjaxFunc();
    twitterStream.stream_open = false;

    this.$button.prop("disabled", true);
    setTimeout( function() {
        twitterStream.$button.text("Start Stream");
        twitterStream.$button.prop("disabled", false);
        console.log("Ready for streaming");
    }, 5 * 1000);
    console.log("Stream Closed");
}

twitterStream.getTweets = function() {
    var queryId = setInterval( function() {
        console.log("querying Twitter...");
        twitterStream.getTweetsAjaxFunc();
    }, this.queryInterval );

    return queryId;
}

twitterStream.getTweetsAjaxFunc = function() {
    jQuery.ajax({
        type: "GET",
        url: twitterStream.get_tweets_url,
        data: {"bad_hashtags" : twitterStream.bad_hashtags},
        dataType: "json",
        success: function(res) {
            if (res.server_stream == undefined || !res.server_stream) {
                console.log("server closed stream!");
                twitterStream.closeStream();
            }

            if (res.tweets != undefined && res.tweets != null) {
                res.tweets = JSON.parse(res.tweets);

                if ( res.tweets instanceof Array && res.tweets.length > 0) {
                    twitterStream.tweets.push(res.tweets);
                    twitterStream.addTweetLayer();
                }
            }
            console.log(res);

        },
        error: function(e, msg) {
            twitterStream.closeStream();
            console.log(e.status + " - " + e.statusText + " [" + msg + "]");
            console.log(e);
        }
    }); //ajax
}

twitterStream.addTweetLayer = function() {
    var features = [];

    for (var t of twitterStream.tweets[twitterStream.tweetIndex]) {

        var dateStr = new Date(parseInt(t.timestamp_ms));
        var imageUrl = null;

        // Add profile pic, twitter handler, and user's name to popup
        var popupContent = '<div class="tweet-popup"><div class="tweet-popup-header">' +
                        '<img src="' + t.user.profile_image_url_https + '"/>' +
                        '<span><h5>@' + t.user.screen_name + '</h5><h6>(' + t.user.name + ')</h6></span></div>' +
                        '<p>' + t.text + '</p><p>Posted today at ' + dateStr.toLocaleTimeString() + '</p>';

        // Adds image, if one exists, to popup
        if ( ("media" in t.entities) && (t.entities.media.length > 0) ) {
            var photo = t.entities.media[0];
            if ( photo.type !== "photo" ) {
                return;
            }
            imageUrl = photo.media_url_https;
            var image = '<div class="tweet-img"><img style="width:125;height:125;" src="'+imageUrl+'"/>' +
                        '<span><a href="#">Click to see full sized image</a></span></div>';
            popupContent = popupContent + '<p>' + image + '</p>';
        }

        // Adds removal and irrelevant buttons to popup
        popupContent +=  '<div data-id="' + twitterStream.feature_id + '"><a href="#" class="irrel-tweet">Flag as ' +
                        'Irrelevant</a>&nbsp;|&nbsp;<a href="#" class="remove-tweet">Remove from Map</a>' +
                        '&nbsp;|&nbsp;<a href="#" class="save-tweet">Save Tweet</a></div>';

        // Closes wrapper div
        popupContent += '</div>';

        var feature_json = {
            type: "Feature",
            properties: {
                id: twitterStream.feature_id++,
                text: t.text,
                source: 'Twitter',
                image: imageUrl,
                place: t.place,
                lang: t.lang,
                username: t.user.name,
                screen_name: t.user.screen_name,
                profile_pic_url: t.user.profile_image_url_https,
                twitter_verified: t.user.verified,
                tweet_id: t.id,
                timestamp: t.created_at,
                hashtags: t.entities.hashtags,
                popupContent: popupContent
            },
            // Note: coordinates field is GeoJson ready, the geo field isn't
            // Even though they share the same data (for the most part)
            geometry : t.coordinates
        }

        t.feature_json = feature_json;
        features.push(feature_json);
    }
    twitterStream.tweetIndex++;

    console.log("adding data to twitter layer...");
    twitterStream.tweetLayer.addData(features);
}

twitterStream.irrelevantTweet = function() {
    console.log("irrelevant tweet");
    var markerId = $(this).parent().attr('data-id');
    markerId = parseInt(markerId);

    var layerList = twitterStream.tweetLayer.getLayers();
    for ( var layer of layerList ) {
        if (layer.feature.properties.id === markerId) {
            twitterStream.tweetLayer.removeLayer(layer);
            twitterStream.bad_hashtags.concat(layer.properties.feature.hashtags);
            console.log(twitterStream.bad_hashtags);
        }
    }
}

twitterStream.removeTweet = function() {
    console.log("removing tweet");
    var markerId = $(this).parent().attr('data-id');
    markerId = parseInt(markerId);

    var layerList = twitterStream.tweetLayer.getLayers();
    for ( var layer of layerList ) {
        if (layer.feature.properties.id === markerId) {
            twitterStream.tweetLayer.removeLayer(layer);
        }
    }
}

//twitterStream.removeFromMap = function(markerId) {
//    var layerList = twitterStream.tweetLayer.getLayers();
//    for ( var layer of layerList ) {
//        if (layer.feature.properties.id === markerId) {
//            twitterStream.tweetLayer.removeLayer(layer);
//        }
//    }
//}