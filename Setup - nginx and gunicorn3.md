# How to run python flask app on nginx & gunicorn — 

**Pre-requisites:**  
install python3 (`sudo apt-get install python3`)  
install pip3 (a python package manager) (`sudo apt-get python3-pip`)  
install flask (`pip3 install flask`)  

Now,  
To install `nginx`, run below cmd:  

```shell
ubuntu@ip-172-31-42-44:~/flask$ sudo apt-get install nginx
```

To install `gunicorn`, run below cmd:  

```shell
ubuntu@ip-172-31-42-44:~/flask$ sudo apt install gunicorn
```

The above cmd will install both gunicorn (compatible with python2) and gunicorn3 (compatible with python3)  


let us create a tiny python flask hello-world app like below:  

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>Hello World!!</h1>"
#if __name__ == "__main__":
#    app.run(host='0.0.0.0',port=8080)
```

to run as standalone, use this cmd:  
```shell
ubuntu@ip-172-31-42-44:~/flask$ sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=8080
 * Serving Flask app "app.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

However, on prodution server, we should not run it as standalone as evident form the above log.  

we should run the python app like this:  To run a python flask app web server:  

```shell
ubuntu@ip-172-31-42-44:~/flask$ gunicorn3 app:app
[2022-01-02 20:39:40 +0000] [13299] [INFO] Starting gunicorn 20.0.4
[2022-01-02 20:39:40 +0000] [13299] [INFO] Listening at: http://127.0.0.1:8000 (13299)
[2022-01-02 20:39:40 +0000] [13299] [INFO] Using worker: sync
[2022-01-02 20:39:40 +0000] [13301] [INFO] Booting worker with pid: 13301
[2022-01-02 20:49:52 +0000] [13299] [INFO] Handling signal: int
[2022-01-02 20:49:52 +0000] [13301] [INFO] Worker exiting (pid: 13301)
```

Let us understand, why're we using nginx & gunicorn both at a time,  

The below is taken from [here](https://www.youtube.com/watch?v=fbljSY54u20)  
gunicorn is basically a python `web server gateway interface`, in short WSGI.  
which works with a number of web-framework  
Unicorn will create a unix socket and it'll server the response to the nginx request via web server gateway interface protocol  
so, the concept is:  
nginx will face the outside world of the internet, so nginx will directly server the media files,  
for ex: static files like images, css, directly from the file system,  
nginx can not directly communicate with the flask application,  
we need something in between the web server i.e. nginx and our flask application.  
we're using `unicorn` to run as an interface b/w webserver and flask application,  
`unicorn` will feed the request from web to applciation and return the response back to web server  

![image](https://user-images.githubusercontent.com/26399543/147892888-c68294d8-101f-4aef-9041-646f944bb10b.png)  

As the setup has been completed, so let us follow for the next steps [here](https://github.com/TheCodeCache/security/blob/master/SSL%20Certificate%20-%20Self%20Sign-In.md)  
