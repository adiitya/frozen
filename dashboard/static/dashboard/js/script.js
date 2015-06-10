
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
                    //If Ip was new then add a new tile
                    if(!('duplicate' in data))
                        dashboard.manageTile.add($('#add_form [name="ip"]').val());
                    $('#add_form [name="ip"]').val('');
                    $('#add_form [name="polling_time"]').val('');
                }
                setTimeout(function() {
                    $('#add_response').html('');
                }, 2000);
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
                setTimeout(function() {
                    $('#delete_response').html('');
                }, 2000);
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
            var row = 1, col = 1, last_col = 0, flag = 0;
            $("#tiles").find('li').each(function(li){
                row = parseInt($(this).attr("data-row"));
                col = parseInt($(this).attr("data-col"));
                if((last_col+1)!=col && (col+4)!=last_col)
                {   flag = 1;
                    col--;
                    if(col==0) {
                        row--;
                        col = 5;
                    }
                    return false;
                }
                last_col = col;
            });
            if(flag==0)
                col++;
            if(col==6) {
                col = 1;
                row++;
            }
            var tile = '<li id = "'+dashboard.helpers.transformIp(Ipdata['name'])+'" data-row="'+ row +'" data-col="' + col + '" data-sizex="1" data-sizey="1" class="gs_w">'
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
            //This ip is separated by "_" instead of "." 
            data = dashboard.fetchIpData.action(dashboard.helpers.reversetransformIp(ip),function(Ipdata){
                var stat = '';
                if(Ipdata['status']==null)
                    stat = "N/A";
                else if(Ipdata['status']=="200"){
                    if($('#'+ip+' div').hasClass('down')){
                        $('#'+ip+' div').removeClass("down");
                        $('#'+ip+' div').addClass('up-'+Math.floor((Math.random() * 4)));
                    }
                    stat = "UP";
                }
                else{
                    for(var i=0; i < 4; i++){
                        if($('#'+ip+' div').hasClass('up-'+i))
                            $('#'+ip+' div').removeClass('up-'+i);
                    }
                    if(!$('#'+ip+' div').hasClass('down'))
                        $('#'+ip+' div').addClass('down')
                    stat = "DOWN";
                }
                $('#'+ip+' div h2').html(stat);
                $('#'+ip+' div p').html("Last fetched: "+Ipdata['last_fetched']);
            });
        }
    };

    dashboard.manageTile.callUpdaterForEachTile();
});