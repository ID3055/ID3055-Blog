##ID3055'blog
### Authors
* [ID3055](https://github.com/ID3055)

### TODO

* 

### requirements

* [requirements.txt](https://github.com/ID3055/ID3055-Blog/blob/master/re.txt)

pip install -r requirements.txt

### 启动前需要做的事

* 在app/config.py中配置数据库


### 数据库初始化方法

* python3.7 manage.py db init
* python3.7 manage.py db migrate -m  "initial migration"
* python3.7 manage.py db upgrade


### Test Command

* python manage.py runserver

### 