from flask import Flask, request, redirect
import N6700C


app = Flask(__name__)
num = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p><br><a href='poweroff'>Power off</a><br><a href='poweron'>Power on</a>"

@app.route('/test/')
def test():
    return 'ceshiceshi'

@app.route('/<num>/')
def var(num):
    return f'var {num}'

@app.route('/poweron/')
def poweron():
    N6700C.poweron()

@app.route('/poweroff/')
def poweroff():
    N6700C.poweroff()

@app.route('/power/', methods=['POST', 'GET'])
def power():
    if request.method == 'POST':
        if request.form['status'] == 'on':
            N6700C.poweron()
            return redirect('/static/Power.html')
        else:
            N6700C.poweroff()
            return redirect('/static/Power.html')
    else: 
        return redirect('/static/Power.html')