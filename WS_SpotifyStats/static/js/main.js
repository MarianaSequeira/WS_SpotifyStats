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

var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onPlayerReady(event) {
	event.target.playVideo();
	check_time(event.target.getVideoUrl().split("=")[1])
}

function check_time(yt_id) {
	var prog = dict[yt_id].getCurrentTime()/dict[yt_id].getDuration() * 100;
	$('#progress'+yt_id).css('width', prog+"%");
	var time = dict[yt_id].getCurrentTime().toFixed(2);
	var minutes = Math.floor(time / 60);
	var seconds = time - minutes * 60;
	var formatted = minutes.toFixed(0).toString().padStart(2, '0') + ':' + seconds.toFixed(0).toString().padStart(2, '0');
	$('#curr_time'+yt_id).text(formatted);
	time = dict[yt_id].getDuration().toFixed(2)
	minutes = Math.floor(time / 60);
	seconds = time - minutes * 60;
	formatted = minutes.toFixed(0).toString().padStart(2, '0') + ':' + seconds.toFixed(0).toString().padStart(2, '0');
	$('#duration'+yt_id).text(formatted);
	console.log('#progress'+yt_id + " -> " +dict[yt_id].getPlayerState());
	setTimeout(check_time, 1000, yt_id);

}

function playVideo(video_id) {

	if(video_id in dict){
		dict[video_id].pauseVideo();
		dict[video_id].playVideo();
	}else{
		let player = new YT.Player("player"+video_id, {
		height: "320",
		width: "320",
		videoId: video_id,
		playerVars: {
		  'playsinline': 1
		},
		events: {
			onReady: onPlayerReady
		}
		});
		dict[video_id] = player
	}
}

function pauseVideo(video_id) {
    dict[video_id].pauseVideo();
}

var dict = {};

