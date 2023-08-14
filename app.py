# flaskモジュールからFlaskクラスをインポート
from flask import Flask, render_template, request, redirect, session

# sqlite3をインポート
import sqlite3
import random


# Flaskクラスをインスタンス化してapp変数に代入
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gacha")
def mikan_gacha():

    # 
    conn = sqlite3.connect("mikanDB.db")

    # クエリの結果をカラム名で取得できる
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # データベースからidを抽出
    c.execute("SELECT id FROM mikans ORDER BY id ASC")

    # idをリストに変換
    items = [d["id"] for d in c.fetchall()]

    # idをランダムで選択
    item = random.choice(items)

    # データベースからidと同じ柑橘を抽出
    c.execute("select * from mikans where id = ?", (item,))

    # 柑橘データを辞書型に変換
    mikan_data = dict(c.fetchone())

    # データベースの接続を終了
    c.close()

    print(mikan_data)

    return render_template("gacha.html", mikan_data=mikan_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


# スクリプトとして直接実行した場合
if __name__ == "__main__":
    # FlaskのWEBアプリケーションを起動
    app.run(debug=True)
