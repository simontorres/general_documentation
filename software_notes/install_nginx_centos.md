# Installation of NGINX on Centos 7

Based on [this blog](https://www.cyberciti.biz/faq/how-to-install-and-use-nginx-on-centos-7-rhel-7/)

1. Add and configure the repository for nginx

   ```sudo vim /etc/yum.repos.d/nginx.repo```
   
   Then, add the following content.
   
   ```
   [nginx]
   name=nginx repo
   baseurl=http://nginx.org/packages/mainline/centos/7/$basearch/
   gpgcheck=0
   enabled=1
   ```

2. Install nginx

   ```sudo yum install nginx```
   
3. Start the service

   ```sudo systemctl start nginx```
