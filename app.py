from flask import Flask, request, render_template, redirect
from bokeh.plotting import save, output_file
from misc import Regulator

app = Flask(__name__)


def process(data):
    A = 2.0
    Beta = 0.035
    H_min = 0.0
    H_max = 10.0
    T_sim = 2.0
    Tp = 1
    Qd = 0.05
    H = 0

    if not data.isdigit() or float(data) > H_max or float(data) < H_min:
        return "err"
    desired = float(data)
    cont = Regulator(A, Beta, H_min, H_max, T_sim, Tp, Qd, H, desired)
    sampling = cont.getSampling()
    for i in range(int(sampling)):
        cont.correct(i)

    return cont.graph()


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def form_post():
    data = request.form['data']
    p = process(data)
    if p == "err":
        return redirect('http://localhost:5000/error')
    output_file('templates/graph.html')
    save(p)
    return redirect('http://localhost:5000/result/')


@app.route('/error/')
def errorlog():
    return render_template('error.html')


@app.route('/result/')
def result():
    return render_template('graph.html')
