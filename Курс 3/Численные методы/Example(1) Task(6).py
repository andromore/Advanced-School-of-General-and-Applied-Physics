# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:43:03 2022

@author: 425
"""
# y' = u
# u' = -0.1u + y - y^3
# u(0) = 10, y(0) = 1/2

import numpy as np
import matplotlib.pyplot as plt

def f0(u, y):  # она же u'
    return u  # а это u'
    
def f1(u, y):
    # return 0.1*(1-u**2)*(u*np.cos(y))
    return -0.1*u + y - y**3

def Runge_Kutta(u, h):  # описание метода
    y = np.zeros(4000)  # заполнили массивы нулями
    u = np.zeros(4000)
    u[0] = 10  # начальные значения
    y[0] = 0.5
    for i in range(0, 3999):
        k10 = h * f0(u[i], y[i])
        k11 = h * f1(u[i], y[i])
        k20 = h * f0(u[i] + 0.5 * h, y[i] + 0.5 * k10)
        k21 = h * f1(u[i] + 0.5 * h, y[i] + 0.5 * k10)
        k30 = h * f0(u[i] + 0.5 * h, y[i] + 0.5 * k20)
        k31 = h * f1(u[i] + 0.5 * h, y[i] + 0.5 * k20)
        k40 = h * f0(u[i] + h, y[i] + k30)
        k41 = h * f1(u[i] + h, y[i] + k30)
        y[i+1] = y[i] + ((k10 + 2*k20 + 2*k30 + k40) / 6.0)
        u[i+1] = u[i] + ((k11 + 2*k21 + 2*k31 + k41) / 6.0)
    return y

# если хотим производную, возвращаем u

x = np.linspace(0, 400, 4000)
y = Runge_Kutta(x, 0.01)
fig = plt.subplots()    
plt.title("решение уравнения")  # заголовок
plt.xlabel("х")  # ось абсцисс
plt.ylabel("у")  # ось ординат
plt.grid()  # включение отображение сетки
plt.plot(x, y)  # построение графика
plt.show()