$(function(){
    $('#addSchedule').click(function() {
		var nickname = $('#nickname').val();
		var password = $('#password').val();
		var group = $('#group').val();
		
		if (group.length == 5) {
            chrome.runtime.sendMessage (
				{
                    name: nickname,
                    password: password,
                    group: group,
				},
				function(response) {
					result = response.farewell;
					alert(result.summary);				
				}
            );
		}
			
		$('#nickname').val('');		
		$('#password').val('');		
		$('#group').val('');		
    });
});

