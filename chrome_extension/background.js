var server_address = '127.0.0.1:8000'

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        var url = 'http://' + server_address + '/google_calendar/create_events/' + 
                            '?name=' + encodeURIComponent(request.name) +
                            '&password=' + encodeURIComponent(request.password) +
                            '&group=' + encodeURIComponent(request.group);

        fetch(url)
        .then(response => response.json())
        .then(response => sendResponse({farewell: response}))
        .catch(error => console.log(error))

        return true;  // Will respond asynchronously.
    }
);