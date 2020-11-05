Project 4 : API gateway, loadbalancing, microservices  
author    : Alex Mulvaney
class     : CPSC449 - Back-end Engineering
-------------------------------------------

procfile contents: 
    gateway: FLASK_APP=gateway flask run -p $PORT  
    users: env FLASK_APP=users_ms.py flask run -p $PORT  
    timelines: env FLASK_APP=timelines_ms.py flask run -p $PORT  
    app: env FLASK_APP=flaskr flask run -p $PORT  

.env contents:  
    FLASK_APP=flaskr  
    FLASK_ENV=development  
    APP_CONFIG=routes.cfg  


commands:
    flask init     #creates the database and adds two Users(cannot authenticate these two users because password_hash isnt called on them,   
                    you can authenticate newly created users though)
                    
    foreman start -m gateway=1,users=3,timelines=3,app=3  #spins up the microservices


gateway.py
--------------------
-handles all the calls to the API.
-routes each request to a subsequent running service.
-handles authorization for each request.

users_ms.py  
---------------------
this is the users microservice api which allows for users to  
        1) Create Users  
        2) Add/Remove Followers  
        3) Authenticate their account  

USER CREATION AND AUTHENTICATION SERVICES     

urls of interest:  
    -/api/v1/users/createuser [POST] {'username','password','email'}  
    -/api/v1/users/authuser   [authorization] (return JSON {"authorization":bool})

FOLLOWER SERVICES    

urls of interest:
    -/api/v1/users/followers [POST {'username','follow'}, DELETE {'username','remove'}, GET]

timelines_ms.py
-------------------------
this is the timelines microservice api which allows for users to 
        1) Post Tweets to the public timeline, and fetch the public timeline
        2) retrieve posts made by specific users
        3) retrieve a "home timeline" featuring posts made by users that a username follows

POSTING SERVICES

urls of interest:
    -/api/v1/timelines/postTweet [POST] {'username','content'}

TIMELINE SERVICES

urls of interest:
    -/api/v1/timelines/<username>          [GET] 
    -/api/v1/timelines/all                 [GET] 
    -/api/v1/timelines/home/<username>     [GET]

{ with the current schema.sql these following timeline calls will automatically work:
    foreman start
    http GET :PORT/api/v1/timelines/home/admin
    http GET :PORT/api/v1/timelines/Tweets
    http GET :PORT/api/vq/timelines/all
}

queries/
--------
contains all the PugSql commands

flaskr/
-------
handles the db creation into the instance/ folder  
contains the 'flask init' command make flask_app=flaskr in env to use