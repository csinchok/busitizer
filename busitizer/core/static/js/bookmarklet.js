// We're gonna need jquery, though.
var busitizer_server = "http://localhost:9090/";
function busitize(el){
	var url = el.getAttribute('src');
	if (url === null || url === '') {
		return;
	}
	el.style.opacity = 0.75;
	$.ajax(busitizer_server + 'busitize', {
		dataType: "json",
		data: {
			url: url
		},
		statusCode: {
			201: function(){
	    		setInterval(function(){
	    			busitize(el);
	    		}, 3000);
   			},
			202: function(){
	    		setInterval(function(){
	    			busitize(el);
	    		}, 3000);
			},
			200: function(data) {
				el.setAttribute('src', busitizer_server + data['busitized']);
				el.style.opacity = 1.0;
			},
			404: function(){
				el.style.opacity = 1.0;
			}
		}
	})
}
$('img').each(function(index, el){
	busitize(el);
});