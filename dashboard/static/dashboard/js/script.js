
$(document).ready(function(){

    var dashboard = {};

    dashboard.source = {
        delete_ip : "/delete_ip",
        add_ip : "/add_ip",
        ip_status : "/status"
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
    
    dashboard.helpers = {
        transformIp : function(ip){
            var res = ip.split(".");
            return res.join('_'); 
        },
        reversetransformIp : function(ip){
            var res = ip.split("_");
            return res.join('.'); 
        }
    };

    dashboard.manageTile = {
        create : function(Ipdata){
            var max_row =1;
            $("#tiles").find('li').each(function(li){
                row = parseInt($(this).attr("data-row"));
                if(row>max_row)
                    max_row = row;
            });
            max_row++;
             var tile = '<li id = "'+dashboard.helpers.transformIp(Ipdata['name'])+'" data-row="'+ max_row +'" data-col="1" data-sizex="1" data-sizey="1" class="gs_w">'
                      +'<div class="down widget widget-number undefined">'
                      +'<h2 class="value" data-bind="current | shortenedNumber | prepend prefix">N/A</h2>'
                      +'<h1 class="title" data-bind="title">'+Ipdata['name']+'</h1>'
                      +'<p class="updated-at" data-bind="updatedAtMessage">Status not available currently</p>'
                      +'</div>'
                      +'</li>';
            return tile;
        },
        add : function(ip){
            dashboard.fetchIpData.action(ip,function(Ipdata){
                tile = dashboard.manageTile.create(Ipdata);
                $('#tiles').append(tile);
                //Adds min_poll_time in map for the new tile
                ip_time_map[Ipdata['name']] = Ipdata['min_poll_time'];
                dashboard.manageTile.startUpdateTimer(dashboard.helpers.transformIp(Ipdata['name']),Ipdata['min_poll_time']);
            }) ;
        },
        remove : function(ip){  
            $('#'+dashboard.helpers.transformIp(ip)).remove();
        },
        //Starts the loop for the attched updater
        startUpdateTimer : function(ip, polling_time){
            var ip = ip;//This ip is separated with "_" instead of "." ! Change if required using helpers
            setTimeout(function(){
                dashboard.manageTile.updateTile(dashboard.helpers.reversetransformIp(ip));
                dashboard.manageTile.updateTile(ip);
                //Again call the same function in a timeout loop
                dashboard.manageTile.startUpdateTimer(ip,parseInt(polling_time));
            },(5*60000));
        },
        //Calls update timer for all tiles previously loaded
        callUpdaterForEachTile : function(){
            $("#tiles").find('li').each(function(li){
                ip = $(this).attr("id");
                dashboard.manageTile.startUpdateTimer(ip,ip_time_map['ip']);
            });
        },
        updateTile : function(ip){    
            data = dashboard.fetchIpData.action(dashboard.helpers.reversetransformIp(ip),function(Ipdata){
                var stat = '';
                if(Ipdata['status']==null)
                    stat = "N/A";
                else if(Ipdata['status']=="200")
                    stat = "UP";
                else
                    stat = "DOWN";
                $('#'+ip+' div h2').html(stat);
                console.log("aa");
            });
        }
    };

    dashboard.manageTile.callUpdaterForEachTile();
});