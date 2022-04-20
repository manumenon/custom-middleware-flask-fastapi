from flask import Flask, request
from middleware import middleware

app = Flask('DemoApp')

# calling our middleware
app.wsgi_app = middleware(app.wsgi_app)


@app.route('/api', methods=['GET', 'POST'])
def hello():
    return "Hi"


@app.route('/', methods=['GET', 'POST'])
def root():
    return "success"


@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    return "success"


if __name__ == "__main__":
    app.run('127.0.0.1', '5000', debug=True)
