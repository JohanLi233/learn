from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# 配置 MySQL 数据库连接
app.config["MYSQL_HOST"] = "localhost"  # 数据库主机
app.config["MYSQL_USER"] = "root"  # 数据库用户名
app.config["MYSQL_PASSWORD"] = "Johan@2003"  # 数据库密码
app.config["MYSQL_DB"] = "learn_news"  # 数据库名
app.config["PORT"] = "1234"  # 端口

mysql = MySQL(app)  # 初始化 MySQL


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/news/<id>")
def get_news(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM news where id = {id}")  # 执行查询
    results = cur.fetchall()  # 获取所有查询结果
    cur.close()  # 关闭游标
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=app.config["PORT"])
