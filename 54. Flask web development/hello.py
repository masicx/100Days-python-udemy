from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/bye')
def bye():
    return 'Goodbye, World!'

if __name__ == '__main__': # Check if the script is being run directly
    app.run()