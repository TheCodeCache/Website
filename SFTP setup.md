# WinScp setup for File transfer from local to EC2 machine —  

Steps to be followed:  
1. Get the Ip or DNS names `IPv4 public IP` or `Public DNS (IPv4)` of your EC2 instance:  
![image](https://user-images.githubusercontent.com/26399543/147873339-6c2feba4-4c6b-412f-85a0-c024c9ce7257.png)   
2. Use either of the above in the `hostname` field of this WinScp connection settings:  
![image](https://user-images.githubusercontent.com/26399543/147873296-30070f95-1bcb-4864-9f78-ca9be12f32e5.png)  
OR  
![image](https://user-images.githubusercontent.com/26399543/147873507-c9c7f216-1416-4298-9468-28ad6031ca2b.png)  
2. User-name  - `ec2-user`
3. Password - `<your IAM user credential password>`  
4. Click advanced button and provide the ppk file as follows -   
![image](https://user-images.githubusercontent.com/26399543/147873415-8cee9db1-66a7-47df-be7d-b562b82300b6.png)  
5. just log-in

And then, SFTP connection will be established and we will get a window something like this:  
![image](https://user-images.githubusercontent.com/26399543/147873632-890dfcec-7c22-48d1-b3f5-d2fe1caa521b.png)  
