var dashboard = {};

dashboard.source = {
    delete_ip : "/delete_ip",
    add_ip : "/add_ip",
    ip_status : "/status"
}


$(document).ready(function(){
    $('#add_ip_button').click(function() {
        $.ajax({
            type: "GET",
            url: dashboard.source.add_ip,
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
            url: dashboard.source.delete_ip,
            data: {
                ip: $('#delete_form [name="ip"]').val()
            },
            success: function(data) { 
                if(data['error'])
                    $('#delete_response').html('<b>'+data['error']+'</b>');
                else
                    $('#delete_response').html(data['success']);
            }
        });
    });

    dashboard.updateIpStatus = {
        action : function(ip){
            $.ajax({
                type: "GET",
                url: dashboard.source.ip_status,
                data: {
                    ip: ip
                },
                success: function(data) { 
                   //Change data of corresponding tiles 
                }
            });
        }
    };

    dashboard.fetchData = {
        action : function(ip, polling_time, last_fetched){
            current_time = Math.floor((new Date).getTime()/1000);
            //If current time is more than last fetched + polling time
            if(current_time >= (last_fetched + polling_time*60))
                dashboard.updateIpStatus.action(ip);    
        }
    };
});