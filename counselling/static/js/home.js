//Setup preloader on window loading.
$(window).load(function(){
	$('.logo1').fadeOut(800);
	$('.logo2').fadeIn(800);
	//Setup the event handler for page ready event.
	$(document).ready(function(){
		$('.logo2').delay(1000).fadeOut(800, function(){
			$('.main-wrapper').show(0);
			$('.loading-screen').animate({
				opacity: 0,
				top: "-=50",
				height: "toggle"
			}, 2200);
		});
			//Initialise page JS
			init();
		});
});

//Method to setup event handlers for page JS
function init(){
	//Setup the menu functionality
	$('.menu-btn1').click(function(){
		if($('.menu-btn1').hasClass('is-active')){
			$(".menu-btn1").removeClass("is-active");
			$('.menu').slideUp(1000, function(){
				$('.logo-menu-active').hide();
				$('.home-page').removeClass("menu-active");
				// $('.mid-text').removeClass('blurd');
				$('.mid-text').show();
				$('.logo-menu-off').show();
			});
		}else{
			$('.logo-menu-off').hide();
			// $('.mid-text').addClass('blurd');
			$('.mid-text').hide();
			$('.home-page').addClass("menu-active");
			$(".menu-btn1").addClass("is-active");
			$('.header-menu').show();
			$('.logo-menu-active').show();
			$('.menu').slideDown(1000);
		}
	});
	

}
