##ID3055'blog
### Authors
* [ID3055](https://github.com/ID3055)

### TODO

* 

### requirements

* [requirements.txt](https://github.com/ID3055/ID3055-Blog/blob/master/re.txt)

pip install -r requirements.txt


### 调试与部署

* 调试时使用外部环境
* 部署时使用docker环境，通过docker-compose up -d启动会自动开启nginx服务
* virtualenv --no-site-packages venv
* pip3 install -r re.txt

### 启动前需要做的事

* 在app/config.py中配置数据库




### 数据库初始化方法

* python3 manage.py db init
* python3 manage.py db migrate -m  "initial migration"
* python3 manage.py db upgrade

* 初始化role表
* python3 manage.py shell
>>>>Role.insert_roles()

### Test Command

* python manage.py runserver --host=0.0.0.0 --port=80

### 