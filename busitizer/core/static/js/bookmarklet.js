// We're gonna need jquery, though.
var busitizer_server = "http://localhost:9090";
function busitize(el){
	var url = el.getAttribute('src');
	if (url === null || url === '') {
		return;
	}
	$.ajax(busitizer_server + '/busitize', {
		dataType: "json",
		data: {
			url: url
		},
		statusCode: {
			201: function(){
	    		setInterval(function(){
	    			busitize(el);
	    		}, 1000);
   			},
			202: function(){
	    		setInterval(function(){
	    			busitize(el);
	    		}, 1000);
			},
			200: function(data) {
				el.setAttribute('src', 'http://localhost:9090/' + data['busitized']);
			}
		}
	})
}
$('img').each(function(index, el){
	busitize(el);
});