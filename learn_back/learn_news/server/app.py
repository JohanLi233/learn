from flask import Flask, jsonify, make_response, Response, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS
from flasgger import Swagger
import MySQLdb.cursors


app = Flask(__name__)
CORS(app) 

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": '',
            "route": '/',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

# 配置 MySQL 数据库连接
app.config["MYSQL_HOST"] = "localhost"  # 数据库主机
app.config["MYSQL_USER"] = "root"  # 数据库用户名
app.config["MYSQL_PASSWORD"] = "1234"  # 数据库密码
app.config["MYSQL_DB"] = "learn_news"  # 数据库名
app.config["PORT"] = "1234"  #  服务器端口

mysql = MySQL(app)  # 初始化 MySQL

@app.route("/")
def default():
    return redirect("/apidocs")


@app.route("/healthy")
def healthy() -> Response:
    return make_response("OK", 200)


@app.route("/recent_news/<amount>")
def get_recent_news(amount):
    """Get recent news specified by amount.
    ---
    parameters:
      - name: amount
        type: integer
        description: The number of news to be returned.
        in: path
        required: true
    responses:
      200:
        description: Newses in json format.
    """
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT id, title, time, link FROM `news` ORDER BY `time` DESC LIMIT " + str(amount)
        cur.execute(sql)
        results = cur.fetchall()  # Fetch all results
        cur.close()  # Close the cursor
        return jsonify(results), 200  # Return JSON response with HTTP status code 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching news"}), 500


@app.route("/news/<id>")
def get_news(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM news where id = {id}")  # 执行查询
    results = cur.fetchall()  # 获取所有查询结果
    cur.close()  # 关闭游标
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=app.config["PORT"])
