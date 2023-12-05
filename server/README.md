
# AutoRunX-Service

## Setup

### OS

linux

### Python

python version >= 3.9

### Mysql

```sh
apt-get install mysql-server
/usr/bin/mysqladmin -u root password '123456'
mysql -u root -p  # then input password
create database autorunx;  # mysql shell
CREATE USER 'aiden'@'localhost' IDENTIFIED BY 'aiden';
GRANT ALL PRIVILEGES ON *.* TO 'aiden'@'localhost';
```

### Django

Django version >=4.2.5

```sh
pip3 install django
pip3 install websockets
pip3 install mysqlclient
```


## Start Service

Using command below to start the service:
```sh
python manage.py runserver
```

## Manage

Super user:
```
admin/admin
```


## Other Command

Create a Django Project:
```sh
django-admin startproject project_name
```

Create an App for Django project:
```sh
django-admin startapp app_name
```





















