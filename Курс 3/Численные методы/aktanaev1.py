import numpy as np

def f(x, a):
    return a * x - 1 / np.tan(x)  

def ff(x):  # Производная
    return 1 + 1 / (np.sin(x) ** 2)  # Для a=1

# Метод Ньютона
def newton(a, x0, tol=1e-7, maxx=100):
    x = x0
    for i in range(maxx):
        fx = f(x, a)
        if abs(fx) < tol:
            return x, i + 1
        fpx = ff(x)
        if fpx == 0:
            break
        x = x - fx / fpx
    return x, maxx

# Метод секущих
def secant(a, x0, x1, tol=1e-7, maxx=100):
    for i in range(maxx):
        fx0 = f(x0, a)
        fx1 = f(x1, a)
        if abs(fx1) < tol:
            return x1, i + 1
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x_new
    return x1, maxx

# Метод парабол (Мюллера)
def muller(a, x0, x1, x2, tol=1e-7, maxx=100):
    for i in range(maxx):
        fx0 = f(x0, a)
        fx1 = f(x1, a)
        fx2 = f(x2, a)
        
        h0 = x1 - x0
        h1 = x2 - x1
        delta0 = (fx1 - fx0) / h0
        delta1 = (fx2 - fx1) / h1
        
        a_coef = (delta1 - delta0) / (h1 + h0)
        b_coef = a_coef * h1 + delta1
        c_coef = fx2
        
        discriminant = np.sqrt(b_coef**2 - 4 * a_coef * c_coef)
        if abs(b_coef + discriminant) > abs(b_coef - discriminant):
            denom = b_coef + discriminant
        else:
            denom = b_coef - discriminant
        
        x_new = x2 - 2 * c_coef / denom
        
        if abs(f(x_new, a)) < tol:
            return x_new, i + 1
        
        x0, x1, x2 = x1, x2, x_new
    return x2, maxx

a = 1.0

# Начальное предположение
x0_n = 1.0  
x0_sec1, x0_sec2 = 0.5, 1.5  
x0_mul1, x0_mul2, x0_mul3 = 0.4, 0.8, 1.2  

# корни
root_n, steps_n = newton(a, x0_n)
root_sec, steps_sec = secant(a, x0_sec1, x0_sec2)
root_mul, steps_mul = muller(a, x0_mul1, x0_mul2, x0_mul3)

print(f"метод ньютона: корень = {root_n:.7f}, шагов = {steps_n}")
print(f"метод секущих: корень = {root_sec:.7f}, шагов = {steps_sec}")
print(f"метод парабол: корень = {root_mul:.7f}, шагов = {steps_mul}")