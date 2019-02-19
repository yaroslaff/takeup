
# Take Up

Take any HTTP form uploads and save on disk.

## Installation


~~~
pip install -r requirements.txt

mkdir /var/run/takeup
mkdir /var/run/takeup/uploads
mkdir /var/log/takeup

chown www-data /var/run/takeup
chown www-data /var/run/takeup/uploads
chown www-data /var/log/takeup
~~~

### Install apache WSGI module

~~~
apt install libapache2-mod-proxy-uwsgi
a2enmod proxy_uwsgi
~~~

### Example apache config
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

## Running cheats
~~~
uwsgi uwsgi.ini

uwsgi --reload /var/run/takeup/takeup.pid

ps `cat /var/run/takeup/takeup.pid`

~~~
