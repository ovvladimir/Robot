# py -3.7 webpy_.py 127.0.0.1
import web

urls = (
    '/', 'index'
)


class index:
    def GET(self):
        return "Hello, World!"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

'''
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)  # , debug=True)  # host='0.0.0.0'
'''
