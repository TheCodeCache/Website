# Firewall — 

It's basically a `traditional firewall`.  
A traditional firewall is `physical` in nature,  
whereas the `security-group` around aws EC2 instance is a `virtual` firewall,  
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

