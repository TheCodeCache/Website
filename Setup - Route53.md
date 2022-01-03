# DNS configurations through Route53 — 

Step-1: buy a domain from Route53, it charges around $12 per year, which comes around 50 cents per month.  
Step-2: register it with Route53 service from AWS  
Step-3: create a hosted zone
Step-4: Add records like below image:  

![image](https://user-images.githubusercontent.com/26399543/147893187-0aed9a10-451f-4be2-a147-d9998316b216.png)

the IP `13.232.222.62` is a public IP of an EC2 instance machine, where our webapp is hosted.  

this is not an elastic IP, so whenever we need to restart the instance, we need to change `A` record value with the new IP everytime.  

to save from this overhead, we could switch to elastic IP, which is reserved for us, but AWS charges for using ElasticIP.  

