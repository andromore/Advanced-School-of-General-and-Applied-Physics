import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

#аараметры сетки
dim_x = 1000 
dim_y = 70000  
q = 0.1  #устойчивость
delta_x = 2 / dim_x  
delta_t = q * delta_x ** 2  


field = np.zeros((dim_x, dim_y))
x_grid = np.linspace(-1, 1, dim_x) 

#дельта функция(аппроксимированная)
delta = np.zeros(dim_x)
delta[dim_x // 2] = 1 / delta_x  # пик в 0

def f2(y):
    y_xx = np.zeros_like(y)
    y_xx[1:-1] = (np.roll(y, 1)[1:-1] + np.roll(y, -1)[1:-1] - 2 * y[1:-1]) / (delta_x ** 2)
    y_xx[0] = (y[1] - y[0]) / (delta_x ** 2)  
    y_xx[-1] = (y[-2] - y[-1]) / (delta_x ** 2) 
    return y_xx + delta

#метод Рунге-кутты
def rk4_step(f, y, delta):
    k1 = delta * f(y)
    k2 = delta * f(y + k1 / 2)
    k3 = delta * f(y + k2 / 2)
    k4 = delta * f(y + k3)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

field[:, 0] = np.zeros(dim_x)

for i in tqdm(range(1, dim_y)):
    field[:, i] = rk4_step(f2, field[:, i - 1], delta_t)

plt.imshow(field[:, ::20], cmap='hot', aspect='auto', extent=[-1, 1, 0, dim_y * delta_t])
plt.colorbar(label='Значение u(x, t)')
plt.xlabel('x')
plt.ylabel('t')
plt.title('Решение u_t = u_xx + delta(x)')
plt.show()