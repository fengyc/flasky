flasky
============================
学习 flask 的 project ，原始代码库 https://github.com/miguelgrinberg/flasky


开始
----------------------------
安装 virtualenv ，并下载依赖。在 windows 下 ::

    virtualenv .venv
    .venv\Script\activate
    pip install -r requirements.txt

运行 flask::

    python -m flasky.app


数据库更新
----------------------------

修改数据库 model 后，进行更新 ::

    python -m flasky.manage db migrate -m '<更新消息>'
    python -m flasky.manage db upgrade


关于邮箱的 smtp 的设置
----------------------------

在环境变量中设置 smtp 参数，windows 上 ::

    set MAIL_USERNAME=<邮箱用户名>
    set MAIL_PASSWORD=<邮箱口令>
    set FLASKY_ADMIN=<管理员邮箱>
