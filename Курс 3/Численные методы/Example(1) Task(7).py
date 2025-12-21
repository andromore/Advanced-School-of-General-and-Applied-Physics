# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:19:47 2022

@author: 425
"""

from scipy.fft import fft, ifft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

def u0(x):
    return x*np.exp(-8*(x**2))

# Вводим начальные данные и число точек по x и t
x_lb = -1  # левая граница
x_rb = 1   # правая граница
Nx = 100        
dt = 0.05
dx = 0.02   
           
x = np.arange(x_lb, x_rb, dx)
# Массивы для Фурье    
k = np.zeros(Nx)
z = np.zeros(Nx)
u = np.zeros((Nx, Nx), dtype=np.complex64)
  
res = np.zeros((100, 100))
    
for l in range(0, Nx-1):
    u[0][l] = u0(x[l])  # u(x,0)   

k = fftfreq(100)*np.pi*100    

for i in range(1, Nx-1):                
    u[i] = ifft(np.exp(-1j*(k**2)*dt)*fft(u[i-1]))
 
z = (abs(sum((abs(u[25]))**2 - sum((abs(u[48]))**2))))

if z < 10**-5:
    print('1ый интеграл сохраняется')
u = u.real

t = np.arange(0, 5, 0.05)
x = np.arange(-1, 1, 0.02)

fig = plt.subplots()    
plt.title("график функции в момент t=0")  # заголовок
plt.xlabel("x")  # ось абсцисс
plt.ylabel("u(x,0)")  # ось ординат
plt.grid()  # включение отображение сетки
y1 = u[0]
plt.plot(x, y1)  # построение графика
plt.show()

ax = plt.axes(projection='3d')
X, Y = np.meshgrid(x, t)                 
Z = u
ax = plt.axes(projection='3d') 
ax.set_xlabel('координата(м)')
ax.set_ylabel('время(c)')
ax.set_title('u(x,t)')
ax.plot_surface(X, Y, Z, rcount=100, ccount=100, cmap='viridis')
plt.show()