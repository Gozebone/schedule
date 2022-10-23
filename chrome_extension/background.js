server_address = '194.67.111.111:8000'

chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		var url = 'http://' + server_address + '/google_calendar/create_events/?group='+ encodeURIComponent(request.group) ;
		
		fetch(url)
		.then(response => response.json())
		.then(response => sendResponse({farewell: response}))
		.catch(error => console.log(error))
			
		return true;  // Will respond asynchronously.		  
    }
);