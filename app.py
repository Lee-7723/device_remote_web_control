from flask import Flask, request, redirect, jsonify, Response, make_response, render_template
from celery import Celery
from celery.result import AsyncResult
import N6700C_foo as N6700C
from redis import Redis
import time

Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)

# 配置消息代理的路径，如果是在远程服务器上，则配置远程服务器中redis的URL
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
# 要存储 Celery 任务的状态或运行结果时就必须要配置
app.config['RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'
# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['RESULT_BACKEND'])
# 将Flask中的配置直接传递给Celery
celery.conf.update(app.config)
num = 1

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/<num>/')
def var(num):
    return f'var {num}'

@app.route('/power/status/')    #查看power开关状态接口
def check_power_status():
    response = {
    'state': N6700C.querystates(), 
    }
    return jsonify(response)

@app.route('/power/', methods=['POST', 'GET'])
def power():
    if request.method == 'POST':
        #print(int(request.form['cycle']))
        cycle = int(request.form['cycle'])
        voltage = float(request.form['voltage'])
        uptime = float(request.form['uptime'])
        downtime = float(request.form['downtime'])
        a = N6700C.setPowercycle.delay(cycle, voltage, uptime, downtime)    #celery用法，将任务交给后台，delay是apply_async的快捷方式
        #a = setCycle.apply_async(args=[cycle, voltage, uptime, downtime])
        print(a.id)
        print(a.status)
    
    if N6700C.queryerrors()==False and 'a' in locals().keys():
        #print(N6700C.querystates())
        task = {'task_id': a.id}
    else:
        #print(N6700C.querystates())
        task = {'task_id': 'no task running'}
    return render_template('Power.html', task=task, state=N6700C.queryerrors()) #向浏览器返回html响应，并在返回的响应中记录task_id，方便标记任务，同时用于浏览器查询任务状态
    
# @celery.task(bind=True)#已弃用，celery加在具体函数所在的py文件里
# def setCycle(self, cycle, voltage, uptime, downtime):
#     N6700C.setPowercycle(cycle, voltage, uptime, downtime)

@app.route('/task_status/<task_id>/')   #任务状态查询接口
def queryTaskstatus(task_id):
    #print('url = '+task_id)
    status = AsyncResult(id=task_id, app=celery)
    if status.state == 'PROGRESS':
        response = {
            'state': status.state,
            'cycle': status.info.get('cycle'),
            'total': status.info.get('total')
        }
    elif status.state == 'SUCCESS' or 'FAILURE':
        response = {
            'state': status.state
        }
    running_tasks = celery.control.inspect().active()['celery@CAGR4NXRAO']  #他人登入时可以看Current task状态来判断仪器是否被占用。
    if len(running_tasks)!=0:
        #print(running_tasks[0]['name'])
        response['current_task'] = running_tasks[0]['name']
    else:
        #print('no task running')
        response['current_task'] = 'no task'
    return jsonify(response)    #以json形式返回数据，网页中用ajax向此接口进行查询

@app.route('/kill_task/<task_id>')  #终止任务接口
def killTask(task_id):
    task = AsyncResult(id=task_id, app=celery)
    task.revoke(terminate=True)



    
if __name__=='__main__':
    app.run(debug=True)