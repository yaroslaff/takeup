# Take Up

Take any HTTP form uploads and save on disk.

## Installation


~~~
pip install -r requirements.txt

mkdir /var/log/takeup
chown www-data /var/log/takeup

mkdir /home/takeup-uploads
mkdir /home/takeup-uploads/tmp
mkdir /home/takeup-uploads/new
chown -R www-data /home/takeup-uploads/
~~~

### Install systemd service
edit uwsgi.ini and ajdust chdir= to path to this takeup directory (where README and takeup.py )
edit takeup.service and adjust ExecStart= to your path to uwsgi.ini
~~~
cp takeup.service /etc/systemd/system/
~~~

### Apache configuration

#### Install apache WSGI module

~~~
apt install libapache2-mod-proxy-uwsgi
apt install uwsgi-plugin-python3
a2enmod proxy_uwsgi
~~~

#### Example apache config
micro:
~~~
<virtualhost *:80>
    DocumentRoot /var/www/virtual/hashdb/
    ServerName hashdb.okerr.com
    ProxyPass /submit unix:/var/run/takeup/takeup.sock|uwsgi://zzz/
</virtualhost>
~~~

full:
~~~

<VirtualHost *:443>
    ServerName hashdb.okerr.com
    DocumentRoot /var/www/virtual/hashdb.okerr.com/
      
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/hashdb.okerr.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/hashdb.okerr.com/privkey.pem

    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
      
</VirtualHost>

<VirtualHost *:80>
    DocumentRoot /var/www/virtual/hashdb.okerr.com/
    ServerName hashdb.okerr.com
    ProxyPass /submit unix:/var/run/takeup/takeup.sock|uwsgi://zzz/

    RewriteEngine On
    RewriteCond %{HTTPS} !=on
    RewriteCond %{REQUEST_URI} !^/\.well\-known        
    RewriteRule (.*) https://%{SERVER_NAME}$1 [R=301,L]
</VirtualHost>
~~~


### Nginx configuration

#### Example config
~~~
server {
    listen 80;
    server_name hashdb.okerr.com;

    location /.well-known {
        root /var/www/virtual/hashdb.okerr.com/;
    	allow all;
    	try_files $uri =404;
    }

    location / {
     	return 301 https://$host$uri;
    }

    access_log /var/log/nginx/hashdb.log;
    error_log /var/log/nginx/hashdb-error.log;
}

server {
	listen 443 ssl;
	server_name hashdb.okerr.com;

	root /var/www/virtual/hashdb.okerr.com/;

	ssl_certificate     /etc/letsencrypt/live/hashdb.okerr.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hashdb.okerr.com/privkey.pem;
	ssl_protocols 	    TLSv1.2; # TLSv1.1 TLSv1;

	# openssl dhparam -out /etc/nginx/dhparam.pem 4096
	ssl_dhparam /etc/nginx/dhparam.pem;

	ssl_ciphers 'kEECDH+ECDSA+AES128 kEECDH+ECDSA+AES256 kEECDH+AES128 kEECDH+AES256 kEDH+AES128 kEDH+AES256 DES-CBC3-SHA +SHA !aNULL !eNULL !LOW !kECDH !DSS !MD5 !RC4 !EXP !PSK !SRP !CAMELLIA !SEED';
	ssl_prefer_server_ciphers on;

	add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;	
	
	location /submit {
        rewrite  ^/submit(.*) /$1 break;
        include uwsgi_params;
		uwsgi_pass unix:/var/run/takeup/takeup.sock;
		client_max_body_size 10M;
    }

    access_log /var/log/nginx/hashdb.log;
    error_log /var/log/nginx/hashdb-error.log;
}
~~~


## Running cheats
~~~
uwsgi uwsgi.ini

uwsgi --reload /var/run/takeup/takeup.pid

ps `cat /var/run/takeup/takeup.pid`

~~~
