import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline

def equation(x, a):
    return a * x - 1 / np.tan(x)

#корень
def get_root(a, start_guess=1.0):
    solution = fsolve(equation, start_guess, args=(a))
    return solution[0]

#интерполяция
a_values = np.linspace(0.1, 0.9, 7)
root_values = [get_root(a) for a in a_values]

eval_a = np.linspace(0.1, 0.9, 100)

# 1линейная
def linear_interp(x_points, y_points, x_new):
    result = []
    for x in x_new:
        i = 0
        while i < len(x_points)-1 and x_points[i] < x:
            i += 1
        i = max(0, i-1)
        
        if i == len(x_points)-1:
            result.append(y_points[-1])
        else:
            x0, x1 = x_points[i], x_points[i+1]
            y0, y1 = y_points[i], y_points[i+1]
            t = (x - x0)/(x1 - x0)
            result.append(y0 + t*(y1 - y0))
    return np.array(result)

linear_result = linear_interp(a_values, root_values, eval_a)

# 2полиномом нбютона
def newton_poly(x_points, y_points, x_new):
    n = len(x_points)
    table = np.zeros((n, n))
    table[:,0] = y_points
    
    for j in range(1, n):
        for i in range(n-j):
            table[i,j] = (table[i+1,j-1] - table[i,j-1])/(x_points[i+j] - x_points[i])
    
    result = []
    for x in x_new:
        res = table[0,0]
        term = 1.0
        for i in range(1, n):
            term *= (x - x_points[i-1])
            res += term * table[0,i]
        result.append(res)
    return np.array(result)

newton_result = newton_poly(a_values, root_values, eval_a)

#3убический сплайн
spline = CubicSpline(a_values, root_values)
spline_result = spline(eval_a)

plt.figure(figsize=(12, 6))
plt.plot(a_values, root_values, 'ro', label='исходные точки', markersize=8)
plt.plot(eval_a, linear_result, 'b-', label='линейная')
plt.plot(eval_a, newton_result, 'g--', label='ньютон')
plt.plot(eval_a, spline_result, 'm-.', label='сплайн')
plt.xlabel('параметр a')
plt.ylabel('корень x(a)')
plt.title('сравнение методов интерполяции')
plt.legend()
plt.grid()
plt.show()

#аппроксимация
more_a = np.linspace(0.01, 0.99, 50)
more_roots = np.array([get_root(a) for a in more_a])

# 1линейная
X = np.vstack([more_a, np.ones(len(more_a))]).T
k, b = np.linalg.lstsq(X, more_roots, rcond=None)[0]
lin_approx = k*eval_a + b

# 2квадратичная
X = np.vstack([more_a**2, more_a, np.ones(len(more_a))]).T
a2, b2, c2 = np.linalg.lstsq(X, more_roots, rcond=None)[0]
quad_approx = a2*eval_a**2 + b2*eval_a + c2

#3рациональная
def rational_approx(x, p1, p2, q1):
    return (p1*x + p2)/(1 + q1*x)

X = np.vstack([more_a, np.ones(len(more_a)), -more_roots*more_a]).T
p1, p2, q1 = np.linalg.lstsq(X, more_roots, rcond=None)[0]
rat_approx = rational_approx(eval_a, p1, p2, q1)

plt.figure(figsize=(12, 6))
plt.plot(more_a, more_roots, 'ko', label='значения точные', markersize=4)
plt.plot(eval_a, lin_approx, 'b-', label='линейная')
plt.plot(eval_a, quad_approx, 'g--', label='квадратичная')
plt.plot(eval_a, rat_approx, 'm-.', label='рациональная')
plt.xlabel('параметр a')
plt.ylabel('корень x(a)')
plt.title('сравнение методов аппроксимации')
plt.legend()
plt.grid()
plt.show()