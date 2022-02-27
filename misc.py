import math
from bokeh.plotting import figure
from func import json_read, json_write


class Regulator:
    def __init__(self, A, Beta, H_min, H_max, T_sim, Tp, Qd, desired):
        self.A = A
        self.Beta = Beta
        self.H_min = H_min
        self.H_max = H_max
        self.T_sim = T_sim * 3600.0
        self.Tp = Tp
        self.Qd = Qd
        self.H = (json_read('data.json'))['H']
        self.Sampling = self.T_sim / self.Tp
        self.Height = [0.0]
        self.Points = [0.0]
        self.desired = desired
        self.QdMAX = 0.05
        self.QdMIN = 0.0

    def getSampling(self):
        return self.Sampling

    def addPoint(self, i):
        self.Points.append(i)

    def graph(self, start):
        p = figure(title='Simple line example', x_axis_label='Time (s)', y_axis_label='Height (m)')
        p.line(self.Points, self.Height)
        p.x_range.start = start
        return p

    def correct(self, i):
        json = json_read('data.json')
        self.H = float(json['H'])
        if self.H != self.desired:
            e = self.desired - self.H
            Qo = self.Beta * math.sqrt(self.H)
            self.Qd = (e + ((self.Tp * Qo) / self.A)) * (self.A / self.Tp)
            if self.Qd < 0:
                self.Qd = 0
            self.H = (1 / self.A) * ((-1) * Qo + self.Qd) * self.Tp + self.H
            if self.H >= self.H_max:
                self.H = self.H_max
            if self.H <= self.H_min:
                self.H = self.H_min
        json['H'] = self.H
        json_write('data.json', json)
        self.Height.append(self.H)
        self.Points.append(i)



