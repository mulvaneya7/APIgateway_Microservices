# foreman start -m gateway=1,users=3,timelines=3,app=3
gateway: FLASK_APP=gateway flask run -p $PORT
users: env FLASK_APP=users_ms.py flask run -p $PORT
timelines: env FLASK_APP=timelines_ms.py flask run -p $PORT
app: env FLASK_APP=flaskr flask run -p $PORT
