from flask import Flask, request, redirect, jsonify
from celery import Celery
import N6700C


app = Flask(__name__)

# 配置消息代理的路径，如果是在远程服务器上，则配置远程服务器中redis的URL
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
# 要存储 Celery 任务的状态或运行结果时就必须要配置
app.config['RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'
# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# 将Flask中的配置直接传递给Celery
celery.conf.update(app.config)
num = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/<num>/')
def var(num):
    return f'var {num}'

@celery.task
def setCycle(cycle, voltage, uptime, downtime):
    N6700C.setPowercycle(cycle, voltage, uptime, downtime)

@app.route('/power/status/')
def check_power_status():
    response = {
    'state': N6700C.querystates(), 
    }
    return jsonify(response)

@app.route('/power/', methods=['POST', 'GET'])
def power():
    # if request.method == 'POST':
    #     if request.form['status'] == 'on':
    #         N6700C.poweron()
    #     else:
    #         N6700C.poweroff()
    # else: pass

    if request.method == 'POST':
        print(int(request.form['cycle']))
        cycle = int(request.form['cycle'])
        voltage = float(request.form['voltage'])
        uptime = float(request.form['uptime'])
        downtime = float(request.form['downtime'])
        #N6700C.setPowercycle.delay(cycle, voltage, uptime, downtime)
        setCycle.apply_async(args=[cycle, voltage, uptime, downtime])
        print(setCycle.apply_async(args=[cycle, voltage, uptime, downtime]).id)
    
    if N6700C.queryerrors()==False:
        #print(N6700C.querystates())
        return redirect('/static/Power.html?noerror')
    else:
        #print(N6700C.querystates())
        return redirect('/static/Power.html?error')
    

    
if __name__=='__main__':
    app.run(debug=True)