# firewall — 

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

To check the status of physical (traditional) firewall:  

```shell
ubuntu@ip-172-31-42-44:~$ sudo ufw status
```
output:  
```shell
Status: inactive
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

