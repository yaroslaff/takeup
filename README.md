
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

### Example apache config
~~~
<virtualhost *:80>
    DocumentRoot /var/www/virtual/hashdb/
    ServerName hashdb.okerr.com
    ProxyPass /submit unix:/var/run/takeup/takeup.sock|uwsgi://zzz/
</virtualhost>
~~~

## Running cheats
~~~
uwsgi uwsgi.ini

uwsgi --reload /var/run/takeup/takeup.pid

ps `cat /var/run/takeup/takeup.pid`

~~~
