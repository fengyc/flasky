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
