from flask import Flask,render_template,request
from utils import jsonOfXlsWithLink,graphData,search_single,singleGraphData,search_two
import os
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph/<name>')
def graph(name):
    if name not in (os.listdir('.')):
        return render_template('404.html')
    r = graphData(name)
    return json.dumps(r, ensure_ascii=False)
    return render_template(
        'graph.html',
    )


@app.route('/table/<name>')
def table(name):
    if name not in (os.listdir('.')):
        return render_template('404.html')
    d = jsonOfXlsWithLink(name)
    return render_template(
        'table.html',
        thead = d['thead'],
        tbody = d['tbody'],
    )


@app.route('/one/<user>')
def one(user):
    tbody = search_single(user)
    if len(tbody) == 0:
        return render_template('404.html')
    cydata=json.dumps(singleGraphData(user))
    return render_template(
        'one.html',
        user=user,
        tbody=tbody,
        cydata= cydata
    )


@app.route('/two')
def tow():
    u1,u2 = request.args['u1'],request.args['u2']
    return search_two(u1,u2)

if __name__ == '__main__':
    config = dict(
        debug=True,
        # host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
