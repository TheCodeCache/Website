# Firewall — 

It's basically a `traditional firewall`.  
A traditional firewall is `physical` in nature,  
whereas the `security-group` around aws EC2 instance, or a group of instance, is a `virtual` firewall,  
in other words, a virtual firewall such as security-group is programmable.  

To get all the available options on ufw command, run:  
```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw help
```
output:  
```shell
Usage: ufw COMMAND

Commands:
 enable                          enables the firewall
 disable                         disables the firewall
 default ARG                     set default policy
 logging LEVEL                   set logging to LEVEL
 allow ARGS                      add allow rule
 deny ARGS                       add deny rule
 reject ARGS                     add reject rule
 limit ARGS                      add limit rule
 delete RULE|NUM                 delete RULE
 insert NUM RULE                 insert RULE at NUM
 route RULE                      add route RULE
 route delete RULE|NUM           delete route RULE
 route insert NUM RULE           insert route RULE at NUM
 reload                          reload firewall
 reset                           reset firewall
 status                          show firewall status
 status numbered                 show firewall status as numbered list of RULES
 status verbose                  show verbose firewall status
 show ARG                        show firewall report
 version                         display version information

Application profile commands:
 app list                        list application profiles
 app info PROFILE                show information on PROFILE
 app update PROFILE              update PROFILE
 app default ARG                 set default application policy
```

To check all the available applications for which we can add a firewall is as follows:  
```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw app list
```
output:  
```shell
Available applications:
  Apache
  Apache Full
  Apache Secure
  OpenSSH
```

To check the status of physical (traditional) firewall:  
```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw status
```
output:  
```shell
Status: inactive
```

To make the firewall active, we need to enable it:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw enable
```
output:  
```shell
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

Check the status again:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw status
```
output:  
```shell
Status: active
```
but there's no application added to the firewall, let us add one:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw allow apache
```
output:  
```shell
Rule added
Rule added (v6)
```

Check the status again:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw status
```
output:  
```shell
Status: active

To                         Action      From
--                         ------      ----
Apache                     ALLOW       Anywhere
Apache (v6)                ALLOW       Anywhere (v6)
```

As we can see now, there is one application 'apache server' is allowed thorugh firewall, while rest of the traffic will be blocked.  

Now, if we need to deny a particular traffic, we need to do like this:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw deny apache
```
output:  
```shell
Rule updated
Rule updated (v6)
```

Now, check the status again:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw status
```
output:  
```shell
Status: active

To                         Action      From
--                         ------      ----
Apache                     DENY        Anywhere
Apache (v6)                DENY        Anywhere (v6)
```

we can observe that the status is still active, so as long as the status is active i.e. the firewall is enabled,  
since there's **`no`** application whitelisted by the firewall, so, all the traffic will get blocked  

Hence, let us turn the firewall off, so that all the traffic will get whitelisted:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw disable
```
output:  
```shell
Firewall stopped and disabled on system startup
```

As we can see now, the firewall has been turned off, thus it would allow the traffic.  

We can test the above using this code:  

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>Hello World!!</h1>"
#if __name__ == "__main__":
#    app.run(host='0.0.0.0',port=8080)
```

and run the above using:  
```shell
ubuntu@ip-172-31-42-44:~/flask$ sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=8080
# or run at Flask's default port like below: 
ubuntu@ip-172-31-42-44:~/flask$ sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
# or at stadard http port i.e. 80 like this: 
ubuntu@ip-172-31-42-44:~/flask$ sudo FLASK_APP=app.py flask run --host=0.0.0.0 --port=80
```

![image](https://user-images.githubusercontent.com/26399543/147885691-db067df7-31eb-48c9-ac7e-9389fd9870c3.png)  

and then hit the url/dns/Ip in browser, it will work fine as below:  

![image](https://user-images.githubusercontent.com/26399543/147885647-d13fa4ae-dc00-4859-a4ac-e36a197267c7.png)  

or  

![image](https://user-images.githubusercontent.com/26399543/147885584-dd929561-4b1e-4fbf-8552-fce68056c115.png)  

or  

![image](https://user-images.githubusercontent.com/26399543/147885667-7f154806-2eaf-45d8-b31d-257eb6c4ab86.png)  

or  

![image](https://user-images.githubusercontent.com/26399543/147885742-c4aa16f6-b9d7-4a13-9f6f-bd051d8b9077.png)  

or  

![image](https://user-images.githubusercontent.com/26399543/147885700-0b1009c0-5d8d-472c-9ad7-7dbd269041a2.png)  

or  

![image](https://user-images.githubusercontent.com/26399543/147885721-6f39f67e-208f-4333-ac7b-d2118aeddf52.png)  


Had the physical firewall was turned on and this traffic was not configured to be allowed then this'd not have worked  


