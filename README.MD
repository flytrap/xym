# 形意门主页
## doc
/docs api文档


## test
django2 只支持python3哦
```bash
mkvirtualenv xym -p /usr/local/bin/python3
pip install requirements.txt
cp xym/settings/locals.py.example xym/settings/locals.py
python manage.py migrate  # 生成数据库
python manage.py createsuperuser  # 管理员创建
python manage.py runserver  # 启动
```

resources/script/import_data.py # 读取pdf文档，导入数据