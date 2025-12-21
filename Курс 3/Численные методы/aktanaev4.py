import numpy as np
from scipy.optimize import brentq
import time

a_start = 1.0
a_end = 2.0
target_a = 1.5
atol = 1e-5

#счетчики
calls_trap, calls_euler, calls_simpson = 0, 0, 0

def equation(x, a):
    return a * x - 1 / np.tan(x)

def find_x(a):
    global calls_trap, calls_euler, calls_simpson
    x_min = 0.1  
    x_max = np.pi - 0.1 
    try:
        root = brentq(equation, x_min, x_max, args=(a), rtol=1e-12)
        return root
    except ValueError:
    #eсли не нашел корень
        return brentq(equation, 0.01, np.pi/2, args=(a), rtol=1e-12)

#метод трапеций
def trapezoidal(n):
    global calls_trap
    a_vals = np.linspace(a_start, a_end, n)
    y = np.array([find_x(a) for a in a_vals])
    calls_trap += n
    h = (a_end - a_start)/(n-1)
    return h*(np.sum(y) - 0.5*(y[0] + y[-1]))

#метод прямоугольников :(
def euler(n):
    global calls_euler
    a_vals = np.linspace(a_start, a_end, n, endpoint=False)
    y = np.array([find_x(a) for a in a_vals])
    calls_euler += n
    h = (a_end - a_start)/n
    return h * np.sum(y)

#метод симпсона
def simpson(n):
    global calls_simpson
    if n % 2 == 0: n += 1  
    a_vals = np.linspace(a_start, a_end, n)
    y = np.array([find_x(a) for a in a_vals])
    calls_simpson += n
    h = (a_end - a_start)/(n-1)
    return h/3 * (y[0] + y[-1] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-1:2]))

#определение необходимого числа точек
def optimize(method):
    n = 2
    prev = method(n)
    current = method(2*n)
    
    while abs(current - prev) > atol and n < 10000:
        n *= 2
        prev = current
        current = method(2*n)
    
    return 2*n, current

start = time.time()
trap_points, trap_int = optimize(trapezoidal)
trap_time = time.time() - start
print(f"метод трапеций: {trap_points} точек ; время: {trap_time:.4f}c ; вызовы: {calls_trap} ; интеграл: {trap_int:.7f}")

start = time.time()
euler_points, euler_int = optimize(euler)
euler_time = time.time() - start
print(f"метод прямоугольников: {euler_points} точек ; время: {euler_time:.4f}c ; вызовы: {calls_euler} ; интеграл: {euler_int:.7f}")

start = time.time()
simp_points, simp_int = optimize(simpson)
simp_time = time.time() - start
print(f"метод симпсона: {simp_points} точек ; время: {simp_time:.4f}c ; вызовы: {calls_simpson} ; интеграл: {simp_int:.7f}")

x_for_target = find_x(target_a)
print(f"\nрешение {target_a}*x = ctg(x): x ≈ {x_for_target:.7f}")