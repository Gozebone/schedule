$(function(){
    $('#addSchedule').click(function(){
		var group = $('#group').val();
		if (group.length == 5){
            chrome.runtime.sendMessage(
				{group: group},
				function(response) {
					result = response.farewell;
					alert(result.summary);					
				}
            );
		}
			
		$('#group').val('');		
    });
});

