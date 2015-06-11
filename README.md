# Project - Frozen
#App - Dashboard

Dashboard is a Django based, shopify-dashing powered network monitoring tool that can monitor multiple contrail modules (like vRouter Agent) remotely for openstack. 

  -  It uses dashing for front-end rendering.
  - It requires Django 1.8.2 or above (Can be installed from requirements.txt using pip)

##For Developers  
###Models   
  - UserProfile - Contains profile of each user and one-to-one mapping to each of them.
  - Users can only be created by admin user.
  - Ip - contain all IP's being monitored by any user, its address and all reated information.
  - UserIpMap - It maps a user to the Ip he is monitoring(Separate fields are created for all).

###Middleware 
  - Any request coming to the server is first served by the middleware. 
  - It authenticates if the user is logged in and if not redirects the request to the login page.
  - If user is logged in it logs last access time of this user on any interaction with server.
  

###Crons
  - #####SetMinPollTimeCronJob
    -  Runs every 1 minute
    -  Checks all Ip objects in Ip table and updates minimum fetching time.It takes one IP and looks for all users manitoring this IP and among all their polling times, it selects the minimum one.
    -  Since server fetches IP status for each IP independent of who all is montoring it, this min_poll_time helps reducing the number of requests by fetching at latest time required.  

  - ####CleanInactiveUsers
    - Runs every 1 minute   
    - Checks all users and if the last_access is less than some specified time limit we make that user dead and from this users IP list we make those IP's dead which are only being watched by this user.
    - ####FetchIpStatus
      - Runs every 1 minute.
      - check if the minimum poll time + last fetched time for this Ip objects exceeds current time, it fetches status else continue. 
