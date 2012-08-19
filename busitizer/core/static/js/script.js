$(function() {

	$.localScroll.defaults.axis = 'xy';

	$.localScroll({
		lazy:true,
		target: '#content',
		queue:true,
		duration:400,
		hash:false,
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

function poll_url(url, timeout) {
	$.get(url, function(data) {
		if(timeout <= 0) {
			alert("I guess you're just not cool enough to get busitized.");
		} else {
			if(data.completed) {
				$('#screen-4 .inner').html(data.html);
				$('#content').stop().scrollTo('#screen-4', 400);
				window.history.pushState("", "Busitized Photo", data.url);
			} else {
				setTimeout(function() {poll_url(url, timeout - 1);}, 1000);
			}
		}
	});
}

function busitize() {
	$.get('/grab_photos.json', function(data) {
		if(data.success) {
			var url = '/poll_completion/' + data.task_id + '.json';
			poll_url(url, 30);
		} else {
			alert(data.message);
		}
	});
}

function poll(){
    $.ajax({ url: "server", success: function(data){
        //Update your dashboard gauge
        salesGauge.setValue(data.value);

    }, dataType: "json", complete: poll, timeout: 30000 });
};
	
function setAllSizes() {
	var viewportWidth = $(window).width();
	var contentWidth = $("#content").width()
	var sum = 0;
	$('#content .sub').css("width",contentWidth); // Set widths of sections to main area width 
	$('#content .sub').each( function(){ sum += $(this).width(); }); // Find sum of widths of sections
	$('#content .section:first-child').width( sum ); //Set content area scroller to sum of width of sections
}

function share(picture) {
    // calling the API ...
    var obj = {
      method: 'feed',
      link: 'https://developers.facebook.com/docs/reference/dialogs/',
      picture: picture,
      name: 'Gary Busey',
      caption: 'Get a little Busey in your life',
      description: 'I found some extra Busey lying around and I wanted to share it with the world.'
    };

    FB.ui(obj, function(){});
}


$(document).ready(function() {
	setAllSizes();
	$(window).resize(function() {
		setAllSizes();
	});
	
    $(".sharefacebook").click(function(){
    	var url = $(this).attr('data-uri');
		share(url);
    });
 });