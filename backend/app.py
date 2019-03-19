from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    print('Some stuff')
    return 'Hello, World!'

if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)