/*
    HOW IT WORKS -- 
        1. Adding and removing of tiles for each IP takes via ajax request.
        Events while adding :-
         *  It adds to main Db and generates a response for success and calls the managetile.add():
            --Managetile.add() creates a new tile and append it to the screen then starts a new timer for this newly
              created tile which will be updating it with fresh status at regular intervals.
        Events while removing :-
        * It deletes Ip from main Db and then remove the tile from main screen.
        Rest description is above all functions.
    Thing t NOTE !!
        * To select any specific IP tile we provide each ip an id which is equal to the IP address.
        Since css Id's cant be separated with "." so we provide underscores in place of "." just for CSS 
        requirement. There are two function in dashboard.helpers which do it for u
            Ex - dashboard.helpers.transformIp("12.13.14.15") will return "12_13_14_15"
            And for making requests we will need the actual IP format which is done by the other function:
                dashboard.reversetransformIp("12_13_14_15") returns "12.13.14.15".
                So for css id's use the output of transformIp() and for requests to server use the output
                of reversetransformIp().

                Cheers!!!

*/          




$(document).ready(function(){

    var dashboard = {};

    //Any source or link you use to make requests goes here.
    dashboard.source = {
        delete_ip : "/delete_ip",
        add_ip : "/add_ip",
        ip_status : "/status"
    }

    //Invoked when someone hits the add_ip_button
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

    //Invoked when someone hits the delete_ip_button
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

    //It fetches current status of ip provided. Remember the ip provided shoukd be in proper IP format.
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
    
    //Helper functions for modifying IP format
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

    //Functios for managing tiles
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

    //This function is called whenever the page reloads and it starts the timer for 
    //updating the tiles present on screen.
    dashboard.manageTile.callUpdaterForEachTile();

});