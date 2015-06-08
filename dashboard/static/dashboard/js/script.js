
$(document).ready(function(){

    var dashboard = {};

    dashboard.source = {
        delete_ip : "/delete_ip",
        add_ip : "/add_ip",
        ip_status : "/status",
        list_ip : "/list_ip"
    }

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
                else{
                    $('#add_response').html(data['success']);
                    dashboard.manageTile.add($('#add_form [name="ip"]').val());
                    $('#add_form [name="ip"]').val('');
                    $('#add_form [name="polling_time"]').val('');
                }
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
                else{
                    $('#delete_response').html(data['success']);
                    dashboard.manageTile.remove($('#delete_form [name="ip"]').val());
                    $('#delete_form [name="ip"]').val('');
                }
            }
        });
    });

    dashboard.fetchIpData = {
        action : function(ip,handleData){
            $.ajax({
                type: "GET",
                url : dashboard.source.ip_status,
                data : {
                    ip : ip
                },
                success : function(data){
                    handleData(data);
                },
                error : function(){

                }
            });
        }
    };
    
    /*dashboard.renderHomeScreen = {
        action : function(){
            $.get(dashboard.source.list_ip, function(Ip){
                var mainHtml = '',
                total = Object.keys(Ip).length,count=0;
                for(var key in Ip){
                    dashboard.fetchIpData.action(Ip[key]['address'],function(Ipdata){
                        tile = dashboard.makeTile.action(Ipdata);
                        console.log(tile);
                        $('#tiles').append(tile);
                    });
                }   
            });
        }
    };

    dashboard.renderHomeScreen.action();*/
    dashboard.manageTile = {
        create : function(Ipdata){
            var max_row =1;
            $("#tiles").find('li').each(function(li){
                row = parseInt($(this).attr("data-row"));
                if(row>max_row)
                    max_row = row;
            });
            max_row++;
            var tile = '<li data-row="'+ max_row +'" data-col="1" data-sizex="1" data-sizey="1" class="gs_w">'
                      +'<div data-view="Number" id = "'+Ipdata['name']+'" class="down widget">'+Ipdata['status']+'</div>'
                      +'</li>';
            return tile;
        },
        add : function(ip){
            dashboard.fetchIpData.action(ip,function(Ipdata){
                tile = dashboard.manageTile.create(Ipdata);
                $('#tiles').append(tile);
            });
        },
        remove : function(ip){  
            $('#'+ip).remove();
        }
    };

    dashboard.updateIpStatus = {
        action : function(ip){
            data = dashboard.fetchIpData.action(ip);
            $('#'+ip).html(data[status]);
            //Update timeout for this tile
        }
    };


});