$(document).ready(function(){
    $('#add_ip_button').click(function() {
        $.ajax({
            type: "GET",
            url: "/add_ip",
            data: {
                ip: $('#add_form [name="ip"]').val(),
                polling_time: $('#add_form [name="polling_time"]').val()
            },
            success: function(data) {
                if(data['error'])
                    $('#add_response').html('<b>'+data['error']+'</b>');
                else
                    $('#add_response').html(data['success']);
            }
        })
    });

    $('#delete_ip_button').click(function() {
        $.ajax({
            type: "GET",
            url: "/delete_ip",
            data: {
                ip: $('#delete_form [name="ip"]').val()
            },
            success: function(data) { 
                if(data['error'])
                    $('#delete_response').html('<b>'+data['error']+'</b>');
                else
                    $('#delete_response').html(data['success']);
            }
        })
    });

    
});