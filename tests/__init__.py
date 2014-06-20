from flask import Flask
app = Flask(__name__)

from middlewares import AjaxCrawlingMiddleware


@app.route("/foo/")
def hello():
    return """<html>
        <h1>Hello Foo Flask World!</h1>
    </html>"""


app.wsgi_app = AjaxCrawlingMiddleware(app.wsgi_app)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(processes=3)

