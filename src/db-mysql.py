import pymysql


class SQLOperation:
    """
    生成sql的类
    """

    def __init__(self, db_info):
        check_key = ['host', 'user', 'password', 'database', 'port']
        for each_key in check_key:
            if each_key not in db_info:
                raise Exception(f"数据库必须字段：{each_key}不在参数里面")
        self.db_name = db_info['database']
        self.connection = pymysql.connect(host=db_info['host'], user=db_info['user'], password=db_info['password'],
                                          database=db_info['database'], charset="utf8")

    def get_table_cols(self, table_name, db_name=None):
        """
        返回表对应的列
        """
        col_list = []
        db_name = db_name if db_name else self.db_name
        sql = f"show columns from {db_name}.{table_name}"
        with self.connection.cursor() as cursor:
            check_int = cursor.execute(sql)
            if not check_int:
                raise Exception(f"查询表的列出现问题！SQL:{sql}")
            cols = cursor.fetchall()
            for col in cols:
                col_list.append(col[0])
            return col_list

    def create_insert_update_sql(self, table_name, where_col_list=None):
        """
        工具函数---用于生成对应的insert和update语句
        """
        sql = f"show columns from {self.db_name}.{table_name}"
        with self.connection.cursor() as cursor:
            check_result_int = cursor.execute(sql)
            if check_result_int == 0:
                print("通过上述条件查询不到相关数据")
            else:
                results = cursor.fetchall()
                insert_string = "insert into {db_name}.{db_table} ("
                update_string = "update {db_name}.{db_table} set "
                col_string = ''
                col_single_string = ''
                for index in range(len(results)):
                    colname = results[index][0]
                    if colname in ["ID", "Id", "id"]: continue
                    col_string += f"{colname}, "
                    col_single_string += f"'{colname}', "
                    insert_string += f"{colname}, " if index < len(results) - 1 else f"{colname}"
                    update_string += (
                        colname + " = " + '"{' + colname + '}", '
                        if index < len(results) - 1 else colname + " = " + '"{' + colname + '}"'
                    )
                insert_string += ") values ("
                update_string += " where "
                for index in range(len(results)):
                    colname = results[index][0]
                    if colname in ["ID", "Id", "id"]:
                        continue
                    insert_string += '"{' + colname + '}", ' if index < len(results) - 1 else '"{' + colname + '}"'
                insert_string += ")"
                if where_col_list:
                    for index in range(len(where_col_list)):
                        wherecol = where_col_list[index]
                        update_string += (
                            wherecol + ' = ' + '"{' + wherecol + '}" and '
                            if index < len(where_col_list) - 1 else wherecol + ' = ' + '"{' + wherecol + '}"'
                        )
                print(f"插入语句：{insert_string}")
                print(f"更新语句：{update_string}")
                print(f"列名带单引号：{col_single_string}")
                print(f"列名：{col_string}")

    def single_select_sql(self, select_cols, where_cols, where_values,
                          order_by, order_type, table_name, db_name, limit=None):
        """
        生成单表查询的sql的函数
        :params select_cols 需要提取的列数据
        :params where_cols 需要进行过滤的列数据
        :params where_values 过滤列对应的值
        :params order_by 排序的列
        :params order_type 升序还是降序
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的select的sql语句
        """
        sql = 'select '
        for index in range(len(select_cols)):
            sql += select_cols[index] + ", " if index < len(select_cols) - 1 else select_cols[index] + " "
        sql += f'from {db_name}.{table_name} '
        # 如果存在where
        if where_cols:
            sql += "where "
            for index in range(len(where_cols)):
                col_name = str(where_cols[index])
                col_value = str(where_values[index])
                sql += (
                    col_name + ' = ' + '"' + col_value + '" and '
                    if index < len(where_cols) - 1 else col_name + ' = ' + '"' + col_value + '" '
                )
        # 如果存在排序
        if order_by and order_type:
            sql += f"order by {order_by} {order_type}"
        # 如果有limit
        if limit:
            sql += f" limit {int(limit)}"
        return sql

    def single_select_sql_with_orderdict(
            self, select_cols, where_cols, where_values, order_dict, table_name, db_name, limit=None):
        """
        生成单表查询的sql的函数-带多排序的情况
        :params select_cols 需要提取的列数据
        :params where_cols 需要进行过滤的列数据
        :params where_values 过滤列对应的值
        :params order_dict 排序字典
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的select的sql语句
        """
        sql = 'select '
        for col in select_cols:
            sql += f"{col}, "
        sql = sql[:-2] + f' from {db_name}.{table_name} '
        # 如果存在where
        if where_cols:
            sql += "where "
            for index in range(len(where_cols)):
                col_name = str(where_cols[index])
                col_value = str(where_values[index])
                sql += (
                    col_name + ' = ' + '"' + col_value + '" and '
                    if index < len(where_cols) - 1 else col_name + ' = ' + '"' + col_value + '" '
                )
        # 如果存在排序
        if order_dict:
            sql += f"order by "
            for k, v in order_dict.items():
                sql += f"{k} {str(v).upper()}, "
            sql = sql[:-2]
        # 如果有limit
        if limit:
            sql += f" limit {int(limit)}"
        return sql

    def single_update_sql(self, update_dict, table_name, db_name, where_cols=[], where_values=[]):
        """
        生成单表更新的sql的函数
        :params update_dict 需要跟新的列与对应的值的字典
        :params where_cols 过滤的列
        :params where_values 过滤列对应的值
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的update的sql语句
        """
        sql = f'update {db_name}.{table_name} set '
        for key in update_dict.keys():
            if update_dict[key] in ["null", None]:
                sql += key + ' = null, '
            else:
                sql += key + ' = "' + str(update_dict[key]) + '", '
        sql = sql[:-2]
        if where_cols:
            sql += " where "
            for index in range(len(where_cols)):
                if where_values[index] in ["null", None]:
                    sql += str(where_cols[index]) + ' is null and '
                else:
                    sql += str(where_cols[index]) + ' = ' + '"' + str(where_values[index]) + '" and '
            sql = sql[:-5]
        return sql

    def insert_sql(self, insert_dict, table_name, db_name):
        """
        生成单表插入的sql的函数
        :params insert_dict 需要插入的列与对应的值的字典
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的insert的sql语句
        """
        sql = f'insert into {db_name}.{table_name} ('
        before_values_sql = ""
        after_values_sql = ""
        for key, value in insert_dict.items():
            before_values_sql += str(key) + ', '
            if value in ["null", None]:
                after_values_sql += 'null, '
            else:
                after_values_sql += '"' + str(value) + '", '
        before_values_sql = before_values_sql[:-2]
        after_values_sql = after_values_sql[:-2]
        sql += before_values_sql + ") values (" + after_values_sql + ")"
        return sql

    def delete_sql(self, table_name, db_name, where_cols=[], where_values=[]):
        """
        生成单表删除的sql的函数
        :params where_cols 过滤的列
        :params where_values 过滤列对应的值
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的delete语句
        """
        sql = f'delete from {db_name}.{table_name} where '
        for index in range(len(where_cols)):
            if where_values[index] in ["null", None]:
                sql += str(where_cols[index]) + ' is null and '
            else:
                sql += str(where_cols[index]) + ' = ' + '"' + str(where_values[index]) + '" and '
        return sql[:-5]

    def delete_sql_with_in(self, table_name, db_name, where_col, where_values=[]):
        """
        生成单表删除的sql的函数-使用in
        :params where_col 过滤的列
        :params where_values 过滤列对应的值
        :params table_name 表名
        :params db_name 数据库名称
        return 对应的使用with的delete语句
        """
        sql = f'delete from {db_name}.{table_name} where {where_col} in ('
        for value in where_values:
            sql += f"'{value}', "
        return sql[:-2] + ")"

    def __del__(self):
        print("对象结束-释放连接")
        self.connection.close()


class DB(SQLOperation):
    """
    数据库操作类
    rpa_db_info = {
        'host': '192.168.0.191',
        'user': 'root',
        'password': '123456',
        'database': 'rpamakebill',
        'port': '3306'
    }
    db = DB(rpa_db_info)
    select_cols, select_vals, datas = db.select("test", db.cols("test"))
    """
    def __init__(self, db_info, auto_commit=True):
        super(DB, self).__init__(db_info)
        self.auto_commit = auto_commit

    def select(self, table_name, select_cols, where_cols=None, where_vals=None,
               order_dict=None, limit=None, show_sql=False):
        """
        从数据库获取数据
        :params table_name: 表名
        :params select_cols: 需要查询出来的属性的列
        return 列，二维值，前者组合成为的字典列表
        """
        spider_sql = self.single_select_sql_with_orderdict(
            select_cols, where_cols, where_vals, order_dict, table_name, self.db_name, limit)
        if show_sql:
            print(f"通过{where_cols}查询的sql：{spider_sql}")
        with self.connection.cursor() as c:
            check_result_int = c.execute(spider_sql)
            if not check_result_int:
                print(f"表{table_name}里面找不到:{where_cols}, {where_vals}的值")
                return select_cols, [], []
            datas = c.fetchall()
            return select_cols, self.get_list(datas), self.format_list_to_dict(select_cols, datas)

    def insert(self, table_name, insert_dict, show_sql=False):
        """
        把数据添加到数据库
        """
        insert_sql = self.insert_sql(insert_dict, table_name, self.db_name)
        if show_sql:
            print(f"插入表：{table_name}的sql为：{insert_sql}")
        with self.connection.cursor() as c:
            check_result_int = c.execute(insert_sql)
            if not check_result_int:
                raise Exception(f"插入表：{table_name}失败 sql:{insert_sql}")
        ID = self.connection.insert_id()
        if self.auto_commit:
            self.commit()
        print(f"插入表:{table_name} 成功ID:{ID}")
        return ID

    def delete(self, table_name, where_cols=[], where_vals=[], show_sql=False):
        """
        删除数据库里面的数据
        :params where_cols 过滤的列
        :params where_vals 过滤列对应的值
        return 对应的delete语句
        """
        delete_sql = self.delete_sql(table_name, self.db_name, where_cols, where_vals)
        if show_sql:
            print(f"删除表：{table_name}的sql为:{delete_sql}")
        with self.connection.cursor() as c:
            check_result_int = c.execute(delete_sql)
            if not check_result_int:
                print(f"删除表：{table_name}失败 sql:{delete_sql}")
                return False
        if self.auto_commit:
            self.commit()
        print(f"删除表：{table_name}对应的数据成功where_cols：{where_cols} where_vals：{where_vals}")
        return True

    def update(self, table_name, update_dict, where_cols=[], where_vals=[], show_sql=False):
        """
        修改数据库里面的数据
        """
        update_sql = self.single_update_sql(
            update_dict, table_name, self.db_name, where_cols, where_vals)
        if show_sql:
            print(f"修改表：{table_name}的sql为:{update_sql}")
        with self.connection.cursor() as c:
            check_result_int = c.execute(update_sql)
            if not check_result_int:
                print(f"修改表：{table_name}失败 sql:{update_sql}")
                return False
        if self.auto_commit:
            self.commit()
        return True

    def cols(self, table_name):
        """
        获取指定表的列
        """
        return self.get_table_cols(table_name)

    def commit(self):
        """
        提交修改
        """
        try:
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"提交数据库出现问题！:{str(e)}")
            raise e

    @staticmethod
    def format_list_to_dict(select_cols, values):
        """
        把二维列表结果转变为字典列表
        :params select_cols:查询的列
        :params values: 二维列表
        return 字典列表
        """
        result = []
        for value in values:
            result.append({select_cols[index]: value[index] for index in range(len(select_cols))})
        return result

    @staticmethod
    def get_list(results):
        """
        根据查询到的结果返回二维列表
        """
        return_list = []
        for each_result in results:
            return_list.append(list(each_result))
        return return_list
