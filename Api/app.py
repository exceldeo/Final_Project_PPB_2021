from flask import Flask,request

app = Flask(__name__)

@app.route('/test', methods=['POST','GET']) 
def foo():
    data = request.data
    # data = "testing"
    print(data)
    return data



if __name__ == "__main__":
  app.run()