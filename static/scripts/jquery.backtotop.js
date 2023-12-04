/*
Template Name: Yammoe
Author: <a href="https://www.os-templates.com/">OS Templates</a>
Author URI: https://www.os-templates.com/
Copyright: OS-Templates.com
Licence: Free to use under our free template licence terms
Licence URI: https://www.os-templates.com/template-terms
File: Back to Top JS
*/

/*
Initial Go back to top function
Did not make any changes
*/
jQuery("#backtotop").click(function () {
    jQuery("body,html").animate({
        scrollTop: 0
    }, 600);
});
jQuery(window).scroll(function () {
    if (jQuery(window).scrollTop() > 150) {
        jQuery("#backtotop").addClass("visible");
    } else {
        jQuery("#backtotop").removeClass("visible");
    }
});

/*
Detail display function, 
Allow user to read more detail about different vitrual travel when user click "detail"
*/

function toggle(target) {
    const param = jQuery(`#${target}`).html();

    if (param === 'Details') {
        jQuery(`#${target}-detail`).show();
        jQuery(`#${target}`).html('Close');
    } else {
        jQuery(`#${target}-detail`).hide();
        jQuery(`#${target}`).html('Details');
    }
}
/*
Switch picture function
When user click picturees, it will switch to another one
*/

function toggleImg() {
    const src = jQuery('#vv-image').attr('src');
    if (src === 'images/pexels-moose-photos-1036642.jpg') {
        jQuery('#vv-image').attr('src', `images/pexels-moose-photos-1036645.jpg`);
    } else {
        jQuery('#vv-image').attr('src', `images/pexels-moose-photos-1036642.jpg`);
    }
}
