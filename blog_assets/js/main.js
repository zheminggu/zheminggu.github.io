


jQuery(document).ready(function ($) {
	"use strict";

	// ============scroll Up==================
    $(window).scroll(function(){
        if ($(this).scrollTop() > 600) {
            $('.scrollup').fadeIn('slow');
        } else {
            $('.scrollup').fadeOut('slow');
        }
    });
    $('.scrollup').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 1000);
        return false;
    });

	
	//=============smooth scrolling ============
	$('.smoothscroll').on('click', function (e) {
		e.preventDefault();
		var target = this.hash, $target = $(target);
		$('html, body').stop().animate({'scrollTop': $target.offset().top},600, 'swing').promise().done(function () {
			// check if menu is open
			if ($('body').hasClass('menu-is-open')) 
			{
				$('.menu-toggle').trigger('click');
			}
			window.location.hash = target;
		  });
	});
	
	/* ------------------------------------------------------
	 * Flexslider
	 * ------------------------------------------------------ */

		$('.carousel').carousel({
  			interval: 3000,
			pause:false
		});
 
});


