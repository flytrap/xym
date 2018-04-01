# 形意门主页
## doc
/docs api文档

## 功能点
- [x] 数据解析(传承谱-截止到3月23日)
  - 数据问题
    - 找不到父节点
      - 薛振纲
      - 周赡
      - 许纪山
    - 传承辈分错误
      - 李起(6->5)
- [x] 意见反馈
- [x] 传承谱
  - [x] 基础展示
    - [x] 指定根节点任意显示
    - [x] 搜索人
      - 关键字，列出多种传承路线组合供选择,数据会比较多，有点儿慢
      - [ ] 分页
      - [ ] 加载中效果
  - [x] 悬浮框，展示用户详细信息
  - [ ] 主题定制
  - [ ] 自适应，节点过于密集信息覆盖问题
- [ ] 地域分布
  - [ ] 展示门人所在地分布图
  - [ ] 本地名师
- [x] 登录注册
  - [x] 用户信息完善
  - [ ] 极验验证
- [x] 用户绑定
  - [x] 后台绑定(只有自己子节点的权限)
  - [ ] 申请绑定
- [ ] 用户邀请
  - 已绑定用户邀请
    - 给后代添加账号，直接可用(已绑定)
  - 未绑定用户邀请
- [ ] 审核申请
  - 提交申请
  - 审查
- [ ] 站内通知
- [ ] 版权解释
  - [ ] 数据来源
  - [ ] 使用说明
  - [ ] 其他


## test
django2 只支持python3
```bash
mkvirtualenv xym -p /usr/local/bin/python3
pip install requirements.txt
cp xym/settings/locals.py.example xym/settings/locals.py
python manage.py migrate  # 生成数据库
python manage.py createsuperuser  # 管理员创建
python manage.py runserver  # 启动
```

resources/script/import_data.py # 读取pdf文档，导入数据


## 常见错误

出现提交数据没有权限的情况，请注释配置中的如下代码
DRF 配置中的"DEFAULT_AUTHENTICATION_CLASSES"
```python
"rest_framework.authentication.SessionAuthentication"
```
