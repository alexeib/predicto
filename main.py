from flask import Flask, request

app = Flask(__name__)


@app.route('/learn', methods=['POST'])
def learn():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
