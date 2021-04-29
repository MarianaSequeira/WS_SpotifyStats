/* ===================================
--------------------------------------
  SolMusic HTML Template
  Version: 1.0
--------------------------------------
======================================*/


'use strict';

$(window).on('load', function() {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");

	if($('.playlist-area').length > 0 ) {
		var containerEl = document.querySelector('.playlist-area');
		var mixer = mixitup(containerEl);
	}

});

(function($) {
	/*------------------
		Navigation
	--------------------*/
	$(".main-menu").slicknav({
        appendTo: '.header-section',
		allowParentLinks: true,
		closedSymbol: '<i class="fa fa-angle-right"></i>',
		openedSymbol: '<i class="fa fa-angle-down"></i>'
	});
	
	$('.slicknav_nav').prepend('<li class="header-right-warp"></li>');
    $('.header-right').clone().prependTo('.slicknav_nav > .header-right-warp');

	/*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function() {
		var bg = $(this).data('setbg');
		$(this).css('background-image', 'url(' + bg + ')');
	});

	
	$('.hero-slider').owlCarousel({
		loop: true,
		nav: false,
		dots: true,
		mouseDrag: false,
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		items: 1,
		autoplay: true
	});

})(jQuery);

//##########################################
//##########################################

// daqui para a frente

var player;
// This code loads the IFrame Player API code asynchronously. This is the Youtube-recommended script loading method
var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// //  This function is called by YouTube once the the API is ready.It creates an &lt;iframe&gt; and sets up the video player inside.
// function onYouTubeIframeAPIReady() {

// }

// The API will call this function when the video player is ready (in this case, start playing the video).
function onPlayerReady(event) {
    event.target.playVideo();
}

function check_time() {
	var prog = player.getCurrentTime()/player.getDuration() * 100;
	console.log(prog + "%");
	$('#progress').css('width', prog+"%");
	$('#curr_time').text(Math.floor(player.getCurrentTime()));
	$('#duration').text(player.getDuration());
	setTimeout(check_time, 1000);
}

// console.log(document.getElementById("play"));
var init=false;
function playVideo(video_id) {
	if(!init){
		player = new YT.Player("player", {
			height: "320",
			width: "320",
			videoId: video_id,
			events: {
				// API event handlers<
				onReady: onPlayerReady,
				onStateChange: check_time
			}
		});
		init=true;
	}

    player.playVideo();

}
function pauseVideo() {
    player.pauseVideo();
}





