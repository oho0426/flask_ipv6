import sqlite3


class SQLiteDatabase:
    def __init__(self, db_name):
        self.db = None
        try:
            # 连接到指定名称的SQLite数据库文件（如果不存在则创建）
            self.db = sqlite3.connect(db_name)

            # 创建表格（可根据需要自行修改）
            cursor = self.db.cursor()
            create_table_query = '''CREATE TABLE IF NOT EXISTS ipv6_info (id INTEGER PRIMARY KEY AUTOINCREMENT, `uid` VARCHAR(50) NOT NULL, `ipv6address` VARCHAR(50) NOT NULL, `domain` VARCHAR(50), `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP);'''
            cursor.execute(create_table_query)
            self.db.commit()

        except Exception as e:
            print("Error connecting to database:", str(e))

    def insert_data(self, data):
        try:
            cursor = self.db.cursor()
            query = "INSERT INTO ipv6_info(`uid`,`ipv6address`,`domain`) VALUES(?, ?, ?)"
            values = list(data.values())
            values_tp = tuple(values)
            cursor.execute(query, values_tp)
            self.db.commit()
            return True

        except Exception as e:
            print("Error inserting data into table:", str(e))
            return False

    def get_all_data(self):
        try:
            cursor = self.db.cursor()
            query = "SELECT * FROM ipv6_info"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error retrieving all data from the table:", str(e))
            return []

    def get_where_data(self, column='*', where_str=""):
        try:
            cursor = self.db.cursor()
            query = f"SELECT {column} FROM ipv6_info"
            where = where_str
            if len(str(where)) > 0:
                query = f"SELECT {column} FROM ipv6_info {where_str}"

            cursor.execute(query)
            result = cursor.fetchall()
            return result

        except Exception as e:
            print("Error retrieving data from the table:", str(e))
            return []

    def close_connection(self):
        if self.db is not None:
            self.db.close()



if __name__ == '__main__':
    # 测试代码
    database = SQLiteDatabase('example.db')
    # user1 = {'uid': 1, 'ipv6': "2409:8a56:3227:514:a4f0:cb52:1a78:1ee0", 'domain': "111.com"}
    # user2 = {'uid': 2, 'ipv6': '2429:8a56:3227:514:a4f0:cb52:1a78:1ee0', 'domain': "1"}
    # database.insert_data(user1)
    # database.insert_data(user2)
    result = database.get_where_data(column='uid, ipv6address, domain, max(create_time) as create_time', where_str='group by uid')
    print(result)
    database.close_connection()