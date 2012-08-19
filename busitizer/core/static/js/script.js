$(function() {

	$.localScroll.defaults.axis = 'xy';
	
	// Scroll initially if there's a hash (#something) in the url 
	$.localScroll.hash({
		target: '#content',
		queue:true,
		duration:400,
		lazy:true
	});

	$.localScroll({
		lazy:true,
		target: '#content',
		queue:true,
		duration:400,
		hash:true,
		onBefore:function( e, anchor, $target ){
			// The 'this' is the settings object, can be modified
		},
		onAfter:function( anchor, settings ){
			// The 'this' contains the scrolled element (#content)
		}
	});
});

$(function() {
		$( "a.button" ).button();
		$( "#busey-level, #busey-mood" ).slider({
			value:1,
			min: 0,
			max: 2,
			step: 1,
			slide: function( event, ui ) {
				$( "#amount" ).val( "$" + ui.value );
			}
		});
		$( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
	}
);
	
function setAllSizes() {
	var viewportWidth = $(window).width();
	var contentWidth = $("#content").width()
	var sum = 0;
	$('#content .sub').css("width",contentWidth); // Set widths of sections to main area width 
	$('#content .sub').each( function(){ sum += $(this).width(); }); // Find sum of widths of sections
	$('#content .section:first-child').width( sum ); //Set content area scroller to sum of width of sections
}


$(document).ready(function() {
	setAllSizes();
	$(window).resize(function() {
		setAllSizes();
	});
 });