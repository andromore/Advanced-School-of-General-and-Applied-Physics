import numpy
from matplotlib import pyplot as plt

ZERO = 1e-20  # Float error

def doit(method, *args):  # Function-tester
    try:
        print(f"    {method.__doc__} сработал: {method(*args)}")
    except Exception as error:
        print(f"    {method.__doc__} не сработал ({str(type(error)).split('\'')[1]}): {error}")

def plot(method, x, *args):  # Function-plotter
    plt.plot(x, method(x, *args), label=method.__doc__)

# Functions and it's derivatives

def function1(x, a):
    if abs(x) < ZERO:
        return -a
    return numpy.sin(x ** 2) / x - a
    
def derivative1(x, a):
    if abs(x) < ZERO:
        return 1
    return 2 * numpy.cos(x ** 2) - numpy.sin(x ** 2) / (x ** 2)
    
def function2(x, y):
    return (x * y - numpy.cos(x)) ** 2 + numpy.sin(x * y) ** 2
    
def gradient2(x, y):
    dx = 2 * (x * y - numpy.cos(x)) * (y + numpy.sin(x)) + 2 * y * numpy.sin(x * y) * numpy.cos(x * y)
    dy = 2 * x * (x * y - numpy.cos(x)) + 2 * x * numpy.sin(x * y) * numpy.cos(x * y)
    return dx, dy
    
def hessian2(x, y):
    h11 = 2 * (y + numpy.sin(x)) ** 2 + 2 * (x * y - numpy.cos(x)) * numpy.cos(x) + 2 * y ** 2 * numpy.cos(2 * x * y)
    h12 = 2 * (x * y - numpy.cos(x)) + 2 * x * (y + numpy.sin(x)) + 2 * x * y * numpy.cos(2 * x * y)
    h22 = 2 * x ** 2 + 2 * x ** 2 * numpy.cos(2 * x * y)
    return [[h11, h12], [h12, h22]]

def derivative5(x):
    return x - x ** 3

def system5(vector):
    x, y = vector
    return numpy.array([y, derivative5(x)])

# Methods 1

def secant(function: callable,
           x0: float, x1: float,
           *args,
           tol: float = 1e-6, iterations: int = 100):
    """Метод секущих"""
    for iteration in range(iterations):
        fx1 = function(x1, *args)
        if abs(fx1) < tol:
            return x1, iteration
        fx0 = function(x0, *args)
        if abs(fx1 - fx0) < ZERO:
            raise ZeroDivisionError("Oops")
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x_new
        if abs(x1 - x0) < ZERO:
            return x1, iteration
    return x1, iterations

def bisection(function: callable,
              a: float, b: float,
              *args,
              tol: float = 1e-6, iterations: int = 100):
    """Метод деления пополам"""
    assert function(a, *args) * function(b, *args) >= 0, "Function should have different values in a and b"
    for iteration in range(iterations):
        c = (a + b) / 2
        fc = function(c, *args)
        if fc == 0 or (b - a) / 2 < tol:
            return c, iteration
        if function(a, *args) * fc < 0:
            b = c
        else:
            a = c
    return (a + b) / 2, iterations

def newton(function: callable, derivative: callable,
           initial: float,
           *args,
           tol: float = 1e-6, iterations: int = 100):
    """Метод Ньютона"""
    x = initial
    for iteration in range(iterations):
        fx = function(x, *args)
        if abs(fx) < tol:
            return x, iteration
        dfx = derivative(x, *args)
        if abs(dfx) < ZERO:
            raise ValueError("Oops")
        x = x - fx / dfx
    return x, iterations

def chord(function: callable,
          a: float, b: float,
          *args,
          tol: float = 1e-6, iterations: int = 100):
    """Метод хорд"""
    if function(a, *args) * function(b, *args) >= 0:
        raise ValueError("Function should have zero value in [a, b]")
    iter_count = 0
    x_prev = a if abs(function(a, *args)) < abs(function(b, *args)) else b
    for _ in range(iterations):
        iter_count += 1
        x_next = (a * function(b, *args) - b * function(a, *args)) / (function(b, *args) - function(a, *args))
        if abs(x_next - x_prev) < tol:
            return x_next, iter_count
        if function(x_next, *args) * function(a, *args) < 0:
            b = x_next
        else:
            a = x_next
        x_prev = x_next
    raise RuntimeError("Don't make ends meet")
    
# Methods 2

def gradient_descent(function: callable, gradient: callable,
                     x0: float, y0: float,
                     alpha: float = 0.01, iterations: int = 1000, tol: float = 1e-6):
    """Метод градиентного спуска"""
    x, y = x0, y0
    for i in range(iterations):
        grad = numpy.array(gradient(x, y))
        x_new, y_new = numpy.array([x, y]) - alpha * grad
        if numpy.linalg.norm(numpy.array([x_new, y_new]) - numpy.array([x, y])) < tol:
            break
        x, y = x_new, y_new
    return function(x, y), i

def newton2d(function: callable, gradient: callable, hessian: callable,
             x0: float, y0: float,
             iterations: int = 100, tol: float = 1e-6):
    """Метод Ньютона"""
    x, y = x0, y0
    for i in range(iterations):
        grad = numpy.array(gradient(x, y))
        hess = numpy.array(hessian(x, y))
        delta = numpy.linalg.solve(hess, -grad)
        x_new, y_new = numpy.array([x, y]) + delta
        if numpy.linalg.norm(delta) < tol:
            break
        x, y = x_new, y_new
    return function(x, y), i
    
def bfgs(function: callable, gradient: callable,
         x0: float, y0: float,
         alpha: float = 0.01, iterations: int = 100, tol: float = 1e-6):
    """Метод BFGS"""
    x, y = x0, y0
    B = numpy.eye(2)
    g = numpy.array(gradient(x, y))
    for i in range(iterations):
        p = -numpy.linalg.solve(B, g)
        x_new, y_new = numpy.array([x, y]) + alpha * p
        s = numpy.array([x_new, y_new]) - numpy.array([x, y])
        g_new = numpy.array(gradient(x_new, y_new))
        y_k = g_new - g
        B = B + numpy.outer(y_k, y_k) / numpy.dot(y_k, s) - B @ numpy.outer(s, s) @ B / numpy.dot(s, B @ s)
        x, y, g = x_new, y_new, g_new
        if numpy.linalg.norm(g) < tol:
            break
    return function(x, y), i
    
def conjugate_gradient(function: callable, gradient: callable,
                       x0: float, y0: float,
                       alpha: float = 0.01, iterations: int = 100, tol: float = 1e-6):
    """Метод градиентного спуска"""
    x, y = x0, y0
    g = numpy.array(gradient(x, y))
    p = -g
    for i in range(iterations):
        x_new, y_new = numpy.array([x, y]) + alpha * p
        g_new = numpy.array(gradient(x_new, y_new))
        beta = numpy.dot(g_new, g_new) / numpy.dot(g, g)
        p = -g_new + beta * p
        x, y, g = x_new, y_new, g_new
        if numpy.linalg.norm(g) < tol:
            break
    return function(x, y), i

# Methods 3: Interpolation

def newton_poly(x_eval, x_nodes, y_nodes):
    """Интерполяция полиномом Ньютона"""
    n = len(x_nodes)
    F = numpy.zeros((n, n))
    F[:, 0] = y_nodes
    
    for j in range(1, n):
        for i in range(n - j):
            F[i, j] = (F[i+1, j-1] - F[i, j-1]) / (x_nodes[i+j] - x_nodes[i])
    
    result = 0
    for j in range(n):
        term = F[0, j]
        for k in range(j):
            term *= (x_eval - x_nodes[k])
        result += term
    return result

def cubic_spline(x_eval, x_nodes, y_nodes):
    """Интерполяция кубическими сплайнами"""
    x_nodes = numpy.asarray(x_nodes, dtype=float)
    y_nodes = numpy.asarray(y_nodes, dtype=float)
    
    n = len(x_nodes) - 1
    h = numpy.diff(x_nodes)
    
    A = numpy.zeros((n+1, n+1))
    A[0, 0] = A[-1, -1] = 1
    b = numpy.zeros(n+1)
    
    for i in range(1, n):
        A[i, i-1:i+2] = [h[i-1], 2*(h[i-1]+h[i]), h[i]]
        b[i] = 3*((y_nodes[i+1]-y_nodes[i])/h[i] - (y_nodes[i]-y_nodes[i-1])/h[i-1])
    
    M = numpy.linalg.solve(A, b)
    
    coeffs = numpy.zeros((n, 4))
    coeffs[:,0] = y_nodes[:-1]
    coeffs[:,1] = (y_nodes[1:]-y_nodes[:-1])/h - h*(2*M[:-1]+M[1:])/3
    coeffs[:,2] = M[:-1]
    coeffs[:,3] = (M[1:]-M[:-1])/(3*h)
    
    x_eval = numpy.asarray(x_eval)
    y_eval = numpy.zeros_like(x_eval)
    
    for i, x in enumerate(x_eval):
        idx = numpy.searchsorted(x_nodes, x) - 1
        idx = max(0, min(idx, n-1))
        dx = x - x_nodes[idx]
        y_eval[i] = coeffs[idx,0] + coeffs[idx,1]*dx + coeffs[idx,2]*dx**2 + coeffs[idx,3]*dx**3
       
    return y_eval

def hermite_spline(x_eval, x_nodes, y_nodes):
    """Интерполяция кубическими сплайнами Эрмита"""
    x_nodes = numpy.asarray(x_nodes, dtype=float)
    y_nodes = numpy.asarray(y_nodes, dtype=float)
    
    n = len(x_nodes) - 1
    h = numpy.diff(x_nodes)
    
    derivatives = numpy.zeros_like(x_nodes)
    derivatives[1:-1] = (y_nodes[2:] - y_nodes[:-2]) / (x_nodes[2:] - x_nodes[:-2])
    derivatives[0] = (y_nodes[1] - y_nodes[0]) / h[0]
    derivatives[-1] = (y_nodes[-1] - y_nodes[-2]) / h[-1]

    coeffs = numpy.zeros((n, 4))
    coeffs[:, 0] = y_nodes[:-1]
    coeffs[:, 1] = derivatives[:-1]
    coeffs[:, 2] = (3*(y_nodes[1:] - y_nodes[:-1])/h - 2*derivatives[:-1] - derivatives[1:])/h
    coeffs[:, 3] = (2*(y_nodes[:-1] - y_nodes[1:])/h + derivatives[:-1] + derivatives[1:])/h**2
    
    x_eval = numpy.asarray(x_eval)
    y_eval = numpy.zeros_like(x_eval)
    
    for i, x in enumerate(x_eval):
        idx = numpy.searchsorted(x_nodes, x) - 1
        idx = max(0, min(idx, n-1))
        dx = x - x_nodes[idx]
        y_eval[i] = coeffs[idx, 0] + coeffs[idx, 1]*dx + coeffs[idx, 2]*dx**2 + coeffs[idx, 3]*dx**3
    
    return y_eval

# Methods 3: Approximation

def linear_regression(x_eval, x_nodes, y_nodes):
    """Линейная регрессия"""
    n = len(x_nodes)
    A = numpy.vstack([x_nodes, numpy.ones(n)]).T
    a, b = numpy.linalg.lstsq(A, y_nodes, rcond=None)[0]
    return a * x_eval + b

def polynomial_regression(x_eval, x_nodes, y_nodes, degree=5):
    """Полиномиальная регрессия"""
    coefficients = numpy.polyfit(x_nodes, y_nodes, degree)
    poly = numpy.poly1d(coefficients)
    return poly(x_eval)

def pade(x_eval, x_nodes, y_nodes, m=2, n=2):
    """Аппроксимация Паде (m - степень числителя, n - знаменателя)"""
    def rational_func(x, *coeffs):
        p = numpy.poly1d(coeffs[:m+1])
        q = numpy.poly1d([1] + list(coeffs[m+1:m+n+1]))
        return p(x) / q(x)
    
    p0 = numpy.random.randn(m + n + 1)
    
    from scipy.optimize import curve_fit
    coeffs, _ = curve_fit(rational_func, x_nodes, y_nodes, p0=p0, maxfev=10000)
    
    def pade_eval(x, coeffs, m, n):
        p = numpy.poly1d(coeffs[:m+1])
        q = numpy.poly1d([1] + list(coeffs[m+1:m+n+1]))
        return p(x) / q(x)
    
    return pade_eval(x_eval, coeffs, m, n)

# Methods 4

def trapezoidal(parameters, roots):
    """Метод трапеций"""
    integral = 0.0
    for i in range(len(parameters)-1):
        da = parameters[i+1] - parameters[i]
        integral += 0.5 * (roots[i] + roots[i+1]) * da
    return integral

def simpsons(parameters, roots):
    """Метод Симпсона"""
    n = len(parameters) - 1
    assert n % 2 != 0, ValueError("Number of intervals must be even for Simpson's rule")
    h = (parameters[-1] - parameters[0]) / n
    integral = roots[0] + roots[-1]
    for i in range(1, n):
        if i % 2 == 0:
            integral += 2 * roots[i]
        else:
            integral += 4 * roots[i]
    return integral * h / 3

def monte_carlo(function, a_min, a_max, samples):
    """Метод Монте-Карло"""
    a_samples = numpy.random.uniform(a_min, a_max, samples)
    x_samples = numpy.array([function(a) for a in a_samples])
    return (a_max - a_min) * numpy.mean(x_samples)

# Methods 5

def central_difference(function, a, step=1e-6):
    """Метод центральных разностей"""
    x_ph = function(a + step)
    x_mh = function(a - step)
    return (x_ph - x_mh)/(2*step)

def runge_romberg(function, a, h0=1e-2, k=2, tol=1e-12):
    """Метод Рунге-Ромберга"""
    def D(h):
        return (function(a + h) - function(a - h))/(2*h)
    
    D1 = D(h0)
    D2 = D(h0/k)
    
    for _ in range(10):
        error = numpy.abs(D1 - D2)
        if error < tol:
            break
        D1, D2 = D2, D2 + (D2 - D1)/(k**2 - 1)
        h0 /= k
    
    return D2

def complex_step_derivative(function, a, step=1e-20):
    """Метод комплексного шага"""
    f_complex = function(a + step*1j)
    return f_complex.imag / step

# Methods 6

def euler(system, initial, times, step):
    """Метод Эйлера (1-го порядка)"""
    n = int((times[1] - times[0]) / step)
    t = numpy.linspace(times[0], times[1], n+1)
    Y = numpy.zeros((n+1, len(initial)))
    Y[0] = initial
    
    for i in range(n):
        Y[i+1] = Y[i] + step * system(Y[i])
    
    return Y[:, 0]

def rk2(system, initial, times, step):
    """Метод Рунге-Кутты (2-го порядка)"""
    n = int((times[1] - times[0]) / step)
    t = numpy.linspace(times[0], times[1], n+1)
    Y = numpy.zeros((n+1, len(initial)))
    Y[0] = initial
    
    for i in range(n):
        k1 = system(Y[i])
        k2 = system(Y[i] + step * k1)
        Y[i+1] = Y[i] + step * (k1 + k2) / 2
    
    return Y[:, 0]

def rk4(system, initial, times, step):
    """Метод Рунге-Кутты (4-го порядка)"""
    n = int((times[1] - times[0]) / step)
    t = numpy.linspace(times[0], times[1], n+1)
    Y = numpy.zeros((n+1, len(initial)))
    Y[0] = initial
    
    for i in range(n):
        k1 = system(Y[i])
        k2 = system(Y[i] + step/2 * k1)
        k3 = system(Y[i] + step/2 * k2)
        k4 = system(Y[i] + step * k3)
        Y[i+1] = Y[i] + step * (k1 + 2*k2 + 2*k3 + k4) / 6
    
    return Y[:, 0]

# Tasks

function = lambda a: newton(function1, derivative1, 0., a)[0]  # Universal solver

# Task 1

a = 0.5
start = 0.
left, right = None, None
print("Задание № 1")
doit(chord, function1, left if left else -1., right if right else 1., a)
doit(secant, function1, left if left else -1., right if right else 1., a)
doit(bisection, function1, left if left else -3., right if right else 2., a)
doit(newton, function1, derivative1, start, a)
del a, start, left, right

# Task 2

x0, y0 = 0.5, 0.5
print("Задание № 2")
doit(bfgs, function2, gradient2, x0, y0)
doit(gradient_descent, function2, gradient2, x0, y0)
doit(newton2d, function2, gradient2, hessian2, x0, y0)
doit(conjugate_gradient, function2, gradient2, x0, y0)
del x0,y0

# Task 3

start = 0.
parameters = list(range(-3, 4)) # 7 значений: -3, -2, -1, 0, 1, 2, 3
roots = []
for parameter in parameters:
    roots.append(newton(function1, derivative1, start, parameter)[0])
x = numpy.linspace(-5., 5., 100)
print("Задание № 3")
print("    Интерполяция: результаты изображены на графике")
plt.figure(31)
plt.plot(parameters, roots, 'ro', label="Точки интерполяции")
plot(newton_poly, x, parameters, roots)
plot(cubic_spline, x, parameters, roots)
plot(hermite_spline, x, parameters, roots)
plt.legend()
plt.title("Задание № 3: Интерполяция")
plt.show()
print("    Аппроксимация: результаты изображены на графике")
plt.figure(32)
plt.plot(parameters, roots, 'ro', label="Точки интерполяции")
plot(linear_regression, x, parameters, roots)
plot(polynomial_regression, x, parameters, roots)
plot(pade, x, parameters, roots)
plt.legend()
plt.title("Задание № 3: Аппроксимация")
plt.show()
del start, x, parameters, roots

# Task 4

a_min = 0.
a_max = 1.
discretization = 1001
points = 100000
def estimate_points(method='trapezoidal'):
    a_test = numpy.linspace(0.1, 0.9, 10)
    x_test = numpy.array([function(a) for a in a_test])
    h = a_test[1] - a_test[0]
    d2x = numpy.gradient(numpy.gradient(x_test, h), h)
    max_d2x = numpy.max(numpy.abs(d2x))
    if method == 'trapezoidal':
        n = numpy.sqrt(1**3 * max_d2x / (12 * 1e-5))
    elif method == 'simpson':
        n = (1**5 * max_d2x / (180 * 1e-5))**(1/4)
    else:
        raise ValueError("Unknown method")
    return int(numpy.ceil(n))
parameters = [i / discretization for i in range(0, discretization + 1)]
roots = [function(parameter) for parameter in parameters]
print("Задание № 4")
print(f"    Метод трапеций: ({trapezoidal(parameters, roots)}, {estimate_points()})")
print(f"    Метод Симпсона: ({simpsons(parameters, roots)}, {estimate_points("simpson")})")
print(f"    Метод Монте-Карло: ({monte_carlo(function, a_min, a_max, points)}, as lot as possible)")
del a_min, a_max, discretization, points, parameters, roots

# Task 5

a = 0.5
print("Задание № 5")
print(f"    Метод центральных разностей: {central_difference(function, a)}")
print(f"    Метод комплексного шага: {complex_step_derivative(function, a)}")
print(f"    Метод Рунге-Ромберга: {runge_romberg(function, a)}")
del a

# Task 6

initial = numpy.array([2.0, 0.0])
times = (0, 10)
step = 0.01
timeline = numpy.linspace(times[0], times[1], int((times[1] - times[0]) / step + 1))
print("Задание № 6")
print("   Результаты изображены на графике")
plt.figure(6)
plt.plot(timeline, euler(system5, initial, times, step), label="Метод Эйлера (1-го порядка)")
plt.plot(timeline, rk2(system5, initial, times, step), label="Метод Рунге-Кутты (2-го порядка)")
plt.plot(timeline, rk4(system5, initial, times, step), label="Метод Рунге-Кутты (4-го порядка)")
plt.legend()
plt.title("Задание № 6")
plt.show()

# Task 7

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
L = 2.0
Nx = 100
Nt = 1000
T = 0.1
dx = L/(Nx-1)
dt = T/Nt
x = numpy.linspace(-1, 1, Nx)
u0 = numpy.zeros(Nx)
u0[Nx//2] = 1.0/dx 
alpha = dt/(2*dx**2)
main_diag = numpy.ones(Nx) * (1 + 2*alpha)
off_diag = numpy.ones(Nx-1) * (-alpha)
A = diags([off_diag, main_diag, off_diag], [-1, 0, 1])
M = diags([1/6, 2/3, 1/6], [-1, 0, 1], shape=(Nx, Nx))
K = diags([-1/dx, 2/dx, -1/dx], [-1, 0, 1], shape=(Nx, Nx))
print("Задание № 7")
# Явная схема
u_exp = u0.copy()
for n in range(Nt):
    u_exp[1:-1] += dt/dx**2 * (u_exp[2:] - 2*u_exp[1:-1] + u_exp[:-2])
    u_exp[0] = u_exp[-1] = 1.0
# Неявная схема - метод Кранка-Николсон
u_imp = u0.copy()
for n in range(Nt):
    b = u_imp.copy()
    b[1:-1] += alpha*(u_imp[2:] - 2*u_imp[1:-1] + u_imp[:-2])
    b[0] = b[-1] = 1.0
    u_imp = spsolve(A, b)
# Метод конечных элементов
A_fe = M + dt*K
u_fe = u0.copy()
for n in range(Nt):
    b = M @ u_fe
    b[0] = b[-1] = 1.0
    u_fe = spsolve(A_fe, b)
print("    Результаты изображены на графике")
plt.figure(7)
plt.plot(x, u0, 'k--', label='Начальное условие')
plt.plot(x, u_exp, label=f'Явная схема')
plt.plot(x, u_imp, label=f'Неявная схема - метод Кранка-Николсон')
plt.plot(x, u_fe, label=f'Метод конечных элементов')
plt.title('Задание № 7')
plt.legend()
plt.show()