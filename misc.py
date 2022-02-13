import math
from bokeh.plotting import figure


class Regulator:
    def __init__(self, A, Beta, H_min, H_max, T_sim, Tp, Qd, H, desired):
        self.A = A
        self.Beta = Beta
        self.H_min = H_min
        self.H_max = H_max
        self.T_sim = T_sim * 3600.0
        self.Tp = Tp
        self.Qd = Qd
        self.H = H
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

    def graph(self):
        p = figure(title='Simple line example', x_axis_label='Time (s)', y_axis_label='Height (m)')
        p.line(self.Points, self.Height)
        return p

    def correct(self, i):
        Qo = self.Beta * math.sqrt(self.H)
        if self.H < self.desired:
            self.Qd = self.QdMAX + Qo
        self.H = (1 / self.A) * ((-1) * Qo + self.Qd) * self.Tp + self.H
        if self.H >= self.H_max:
            self.H = self.H_max
        if self.H == self.desired:
            self.Qd = Qo
        elif self.H > self.desired:
            self.Qd = self.QdMIN
        self.Height.append(self.H)
        self.Points.append(i)


