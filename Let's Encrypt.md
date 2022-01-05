# Secure Web Connection using [`Let's Encrypt`](https://letsencrypt.org/) — 

Using `Let's Encrypt` is way too simple and free of charges, however we need to renew it after every 3 months  
as when I tried it just half an hour before, the validity expires on 05-Apr-2022  

PFB the results after setting up `let's encrypt`:  

![image](https://user-images.githubusercontent.com/26399543/148194948-047e9164-e2c8-436b-97c6-0d53686688fc.png)  

![image](https://user-images.githubusercontent.com/26399543/148194272-e82074e8-74f4-4b1b-be2d-d0a3f031800b.png)  

![image](https://user-images.githubusercontent.com/26399543/148194350-629b3647-5d56-4b99-a35a-943161a10d37.png)  

Certificate Details:  

![image](https://user-images.githubusercontent.com/26399543/148194409-32ea8768-e44e-4dd8-9d1e-651d2ed28824.png)  

![image](https://user-images.githubusercontent.com/26399543/148194619-847935a8-6280-4424-bee0-d5b403004837.png)  

![image](https://user-images.githubusercontent.com/26399543/148194693-cdffb022-7b4f-4d98-a4d6-048fe4a235da.png)  

Now, to achieve all of the above, let us follow the below steps, it's way simple  
Visit this link - https://letsencrypt.org/getting-started/  

search for `Cerbot` ACME client  
or,  
hit [Certbot](https://certbot.eff.org/)  

In the above webpage, there's something like this:  
![image](https://user-images.githubusercontent.com/26399543/148192458-8b093c8a-2b32-4573-861d-2ec7b3e58bc0.png)  

select the appropriate software (web server) and system on which the software is running,  
for ex: in my case, I selected `Nginx` and `Ubuntu 20`  

upon selection, it will populate the steps accordingly in the section down below on the page:  

Step-1:  install `snapd`  
```shell
sudo snap install core; sudo snap refresh core
```
Step-2: Remove existing `certbot`  
```shell
sudo apt-get remove certbot
```
Step-3: Install Certbot  
```shell
sudo snap install --classic certbot
```
Step-4: Prepare the Certbot command  
```shell
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
Step-6: run `certbot` to get and install the certificates  
```shell
sudo certbot --nginx
```
Step-7: Test automatic renewal  
```shell
sudo certbot renew --dry-run
```
the command to renew certbot is installed in one of the following locations:  
- /etc/crontab/
- /etc/cron.*/*
- systemctl list-timers  

To check how I've actually followed the above steps, kindly visit [this](https://github.com/TheCodeCache/Website/blob/master/activity_log_4.txt) and [this](https://github.com/TheCodeCache/Website/blob/master/activity_log_5.txt)  

