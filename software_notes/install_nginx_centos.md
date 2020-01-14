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

# Configuring NGINX

I used information from several sources

[gunicorn docs](http://docs.gunicorn.org/en/latest/deploy.html)

 And since I'm mounting the app on a subpath I used [this post](https://docs.webfaction.com/software/django/config.html#mounting-a-django-application-on-a-subpath)
 
 
1. Edit the file `/etc/nginx/conf.d/default.conf`

   ```sudo vim /etc/nginx/conf.d/default.conf```
   
   It should look like this (though depends on what you want to do).
   
   ```
    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }

        location /gsp/ {
            root /pipeline/webapp/static
            proxy_pass http://localhost:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
   }   
   ```
   
   This is the development server so I just left localhost as `server_name` I also left the default nginx location.
   
2. Restart the service with

   ```sudo systemctl restart nginx`
   
# Notes

1. Since I mounted the app on a subpath, I had to do several changes to the django app.

  a. Add `FORCE_SCRIPT_NAME` without trailing slash so every url resolve will use it. 
  
  ```FORCE_SCRIPT_NAME = '/gsp'```
  
  For instance. If I had settings served at `http://localhost:8000/settings/` with this configuration now will be  `http://localhost/gsp/settings/`
  
 b. Get rid of every static url defined, for instance I had to change the following variables.
 
 From:
 
 ```
 LOGIN_REDIRECT_URL = '/'
 LOGOUT_REDIRECT_URL = '/'
 ```
 
 To:
 ```
 LOGIN_REDIRECT_URL = 'data:index'
 LOGOUT_REDIRECT_URL = 'data:index'
 ```
 
 Where `'data:index'` is defined in the `url.py` file of the app `data`.
 
 Also in the templates replacing
 
 ```<form action='/accounts/logout' method="POST">```
 
 by
 
 ```<form action="{% url 'logout' %}" method="POST">```
