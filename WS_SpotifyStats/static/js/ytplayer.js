$(function() {
  /* Load jPlayer */
   // new jPlayerPlaylist({
	// 		jPlayer: "#jp_video",
	// 		cssSelectorAncestor: "#jp_video_container"
	// 	}, [
	// 		{
	// 			title:"Finding Nemo Teaser",
	// 			m4v: "http://www.jplayer.org/video/m4v/Finding_Nemo_Teaser.m4v",
	// 		},
	// 		{
	// 			type: "youtube", /* <- Remember to add this */
	// 			title: "Finding Dory - Youtube",
	// 			m4v:"https://www.youtube.com/watch?v=cfLob5IYMp8",
	// 		},
	// 		{
	// 			title:"Incredibles Teaser",
	// 			m4v: "http://www.jplayer.org/video/m4v/Incredibles_Teaser.m4v",
	// 		}
	// 	], {
	// 		playlistOptions: {
	// 	    	autoPlay: true
   //     		},
	// 		supplied: "m4v",
	// 		smoothPlayBar: true,
	// 		keyEnabled: false,
	// 	});

	/* Youtube Integration Setup */
	var setupYoutube = function(whereDivTo, width, height) {
		$("<div>").attr("id", "ytplayer").appendTo(whereDivTo);

		onYouTubeIframeAPIReady = function() {
	 		youtubeApi = new YT.Player("ytplayer", {
        		videoId: "cfLob5IYMp8",
				playerVars: {
					"autoplay": 1,
					"color": "white",
					"modestbranding": 1,
					"rel": 0,
					"showinfo": 0,
					"theme": "light"
				},
				events: {
					"onReady": function() {
						$(document).trigger("ready.Youtube");
					},
					"onStateChange": "youtubeStateChange"
				}
			});
	 	}

 		$.getScript("http://www.youtube.com/player_api");
	},
	loadYoutubeListeners = function(player, jplayer, id) {
		var container = $(player.options.cssSelector.gui, player.options.cssSelectorAncestor);

		youtubeStateChange = function(ytEvent) {
 			switch(ytEvent.data) {
 				case -1:
 					$(ytEvent.target.getIframe()).show();
 					$(jplayer).find('video').hide();
				 	container.css({ 'opacity' : 0, 'z-index': -1, 'position' : 'relative' });
				 	container.find('.jp-interface').slideUp("slow");
 				break;

 				case YT.PlayerState.ENDED:
 					$(jplayer).trigger($.jPlayer.event.ended);
 				break;

 				case YT.PlayerState.CUED:
 					$(jplayer).find('video').show();
 					$(ytEvent.target.getIframe()).hide();
 					container.css({ 'opacity' : 1, 'z-index': 0 });
 					container.find('.jp-interface').slideDown("slow");

 			}
		};

 		youtubeApi.loadVideoById(id);
	}

	$(document).on($.jPlayer.event.setmedia, function(jpEvent) {


		var player = jpEvent.jPlayer,
			url = player.status.src;
		console.log(jpEvent.target)


	 	var youtubeId = url.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/)[1]


		if(window['youtubeApi'])
			loadYoutubeListeners(player,jpEvent.target, youtubeId);
		else {

			setupYoutube(jpEvent.target, player.status.width, player.status.height);

		 	$(document).on("ready.Youtube", function() {
		 		loadYoutubeListeners(player, jpEvent.target, youtubeId);
		 	});
		}
	});
});