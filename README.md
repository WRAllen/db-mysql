# db-mysql

# 介绍

这是一个简单的操作mysql数据库的库（底层是基于pymysql，只是做了生成sql和执行的简单功能）。是我在项目中无法使用ORM框架（SQLAlchemy）时候为了不重复写sql语句，并且为了项目后期表变动好修改才自己写了这个操作类。（由于数据库的表过多，并且表结构也不是我设计的，最重要的是不涉及复杂的sql操作，例如left join等，为了方便自己开发才有了这个）

## 优点：

不用重复编写CRUD的sql语句

## 缺点

暂时只支持单表的简单CRUD

## 说明

使用方法也非常简单，通过复制源码到项目，然后进行导包使用，或者是通过pip安装后import使用。

PS：不断更新中，有错误欢迎指出

# 具体使用方法

把数据库基础信息字典传入操作类，进行实例化

```python
rpa_db_info = {
    'host': '192.168.0.191',
    'user': 'root',
    'password': '123456',
    'database': 'rpamakebill',
    'port': '3306'
}
# 实例化db对象 默认自动提 auto_commit=True
db = DB(rpa_db_info)
```

## 一些方便的方法

```python
# 获取一个表的所有列
db.cols("test")
```

## 查询语句

```python
select(self, table_name, select_cols, where_cols=None, where_vals=None, order_dict=None, limit=None, show_sql=False)
# 说明
select(表名, 需要查询的列名, 过滤的列名, 过滤的列名对应的值, 排序的字典, limit限制数量，是否打印生成的SQL)
# 返回值
字段列表，查询到的二维列表，前面二者合起来的字典列表 = db.select(表名, 需要查询的列名)
```

具体使用：

```python
# 简单的查询
cols, vals, datas = db.select("test", db.cols("test"))
# 查询test表里面ID为100的数据
ID = 100
cols, vals, datas = db.select("test", db.cols("test"), ["ID"], [ID])
# 查询test表里面ID为100，并且Name为“wrallen”的数据
Name = "wrallen"
cols, vals, datas = db.select("test", db.cols("test"), ["ID", "Name"], [ID, Name])
# 按照更新时间递减，添加时间递增
order_dict = {
    "DateTime": "DESC",
    "AddTime": "ASC"
}
cols, vals, datas = db.select("test", db.cols("test"), ["ID", "Name"], [ID, Name], order_dict)
# 查询test表里面的ID和Name的默认排序的前10条
cols, vals, datas = db.select("test", ["ID", "Name"], limit=10)
```

## 添加语句

```python
insert(self, table_name, insert_dict, show_sql=False)
# 说明
insert(表名, 插入的数据-字典, 是否打印生成的SQL)
# 返回值
插入成功的ID = db.insert(表名, 插入的数据-字典)
```

具体使用

```python
insert_sql = {
    "Name": "bill"
}
new_id = db.insert("test", insert_sql)
```

## 删除语句

```python
delete(self, table_name, where_cols=[], where_vals=[], show_sql=False)
# 说明
delete(表名, 过滤的列名, 过滤的列名对应的值, 是否打印生成的SQL)
# 返回值-True, 删除失败会报异常
```

具体使用

```python
# 删除test表里面ID为1的数据
db.delete("test", ["ID"], [1])
```

## 更新语句

```python
update(self, table_name, update_dict, where_cols=[], where_vals=[], show_sql=False)
# 说明
update(表名, 更新的字典, 过滤的列名, 过滤的列名对应的值, 是否打印生成的SQL)
# 返回值-True, 更新失败会报异常
```

具体使用

```python
# 更新test表里面ID为1的Name为bill
update_dict = {
    "Name": "bill"
}
db.update("test", update_dict, ["ID"], [1])
```





