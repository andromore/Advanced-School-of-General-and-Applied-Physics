from math import sin, cos, sqrt

ZERO = 1e-20 # Float error

def doit(method, *args): # Function-tester
    try:
        print(f"    {method.__doc__} сработал: {method(*args)}")
    except Exception as error:
        print(f"    {method.__doc__} не сработал ({str(type(error)).split("\'")[1]}): {error}")
        
# Matrix and vector functions

def solve(matrix, vector):
    """Solve `matrix @ x = vector`"""
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    assert (ZERO < det) or (-ZERO > det), f"Matrix determine shouldn't be zero ({det})"
    x1 = (vector[0] * matrix[1][1] - vector[1] * matrix[0][1]) / det
    x2 = (matrix[0][0] * vector[1] - matrix[1][0] * vector[0]) / det
    return x1, x2

def minus(vector):
    """Return `-vector`"""
    return -vector[0], -vector[1]

def scalar(vector, alpha: float):
    """Return `scalar * vector`"""
    return alpha * vector[0], alpha * vector[1]
    
def scalar_m(matrix, scalar):
    """Multiply matrix by scalar"""
    return [[matrix[0][0] * scalar, matrix[0][1] * scalar], [matrix[1][0] * scalar, matrix[1][1] * scalar]]
    
def sum(vector1, vector2):
    """Sum `vector1 + vector2`"""
    return vector1[0] + vector2[0], vector1[1] + vector2[1]
    
def sum_m(matrix1, matrix2):
    """Matrix sum"""
    return [[matrix1[0][0] + matrix2[0][0], matrix1[0][1] + matrix2[0][1]], [matrix1[1][0] + matrix2[1][0], matrix1[1][1] + matrix2[1][1]]]
    
def inner(vector1, vector2):
    """Scalar multiplication = inner product"""
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]
    
def square(vector):
    """Scalar square of vector"""
    return inner(vector, vector)
    
def norm(vector):
    """Get norm of vector"""
    return sqrt(square(vector))
    
def outer(vector1, vector2):
    """Outer multiplication"""
    return [[vector1[0] * vector2[0], vector1[0] * vector2[1]], [vector1[1] * vector2[0], vector1[1] * vector2[1]]]
    
def matrix(matrix1, matrix2):
    """Matrix multiplication"""
    return [[matrix1[0][0] * matrix2[0][0] + matrix1[0][1] * matrix2[1][0], matrix1[0][0] * matrix2[0][1] + matrix1[0][1] * matrix2[1][1]],
            [matrix1[1][0] * matrix2[0][0] + matrix1[1][1] * matrix2[1][0], matrix1[1][0] * matrix2[0][1] + matrix1[1][1] * matrix2[1][1]]]
            
def operator(matrix, vector):
    """Result of `matrix @ vector`"""
    return [matrix[0][0] * vector[0] + matrix[0][1] * vector[1], matrix[1][0] * vector[0] + matrix[1][1] * vector[1]]
    
# Functions and it's derivatives

def function1(x, a):
    if abs(x) < ZERO:
        return -a
    return sin(x ** 2) / x - a
    
def derivative1(x, a):
    if abs(x) < ZERO:
        return 1
    return 2 * cos(x ** 2) - sin(x ** 2) / (x ** 2)
    
def function2(x, y):
    return (x * y - cos(x)) ** 2 + sin(x * y) ** 2
    
def gradient2(x, y):
    dx = 2 * (x * y - cos(x)) * (y + sin(x)) + 2 * y * sin(x * y) * cos(x * y)
    dy = 2 * x * (x * y - cos(x)) + 2 * x * sin(x * y) * cos(x * y)
    return dx, dy
    
def hessian2(x, y):
    h11 = 2 * (y + sin(x)) ** 2 + 2 * (x * y - cos(x)) * cos(x) + 2 * y ** 2 * cos(2 * x * y)
    h12 = 2 * (x * y - cos(x)) + 2 * x * (y + sin(x)) + 2 * x * y * cos(2 * x * y)
    h22 = 2 * x ** 2 + 2 * x ** 2 * cos(2 * x * y)
    return [[h11, h12], [h12, h22]]

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
        x_new, y_new = sum((x, y), minus(scalar(gradient(x, y), alpha)))
        if norm(sum((x_new, y_new), (x, y))) < tol:
            break
        x, y = x_new, y_new
    return function(x, y), i

def newton2d(function: callable, gradient: callable, hessian: callable,
             x0: float, y0: float,
             iterations: int = 100, tol: float = 1e-6):
    """Метод Ньютона"""
    x, y = x0, y0
    for i in range(iterations):
        delta = solve(hessian(x, y), minus(gradient(x, y)))
        x_new, y_new = sum((x, y), delta)
        if norm(delta) < tol:
            break
        x, y = x_new, y_new
    return function(x, y), i
    
def bfgs(function: callable, gradient: callable,
         x0: float, y0: float,
         alpha: float = 0.01, iterations: int = 100, tol: float = 1e-6):
    """Метод BFGS"""
    x, y = x0, y0
    B = [[1, 0], [0, 1]]
    g = gradient(x, y)
    for i in range(iterations):
        x_new, y_new = sum((x, y), scalar(minus(solve(B, g)), alpha))
        s = sum((x_new, y_new), minus((x, y)))
        g_new = gradient(x_new, y_new)
        y_k = sum(g_new, minus(g))
        B = sum_m(sum_m(B, scalar_m(outer(y_k, y_k), 1 / inner(y_k, s))), scalar_m(matrix(matrix(B, outer(s, s)), B), -1 / inner(s, operator(B, s))))
        x, y, g = x_new, y_new, g_new
        if norm(g) < tol:
            break
    return function(x, y), i
    
def conjugate_gradient(function: callable, gradient: callable,
                       x0: float, y0: float,
                       alpha: float = 0.01, iterations: int = 100, tol: float = 1e-6):
    """Метод градиентного спуска"""
    x, y = x0, y0
    g = gradient(x, y)
    p = minus(g)
    for i in range(iterations):
        x_new, y_new = sum((x, y), scalar(p, alpha))
        g_new = gradient(x_new, y_new)
        beta = inner(g_new, g_new) / inner(g, g)
        p = sum(minus(g_new), scalar(p, beta))
        x, y, g = x_new, y_new, g_new
        if norm(g) < tol:
            break
    return function(x, y), i

# Tasks

print("Задание № <Номер>")
print("    Метод <название метода> <сработал/не сработал>: (<минимум функции>, <количество итераций>)")

# Task 1

a = 0.5
start = 0.
left, right = None, None
print("Задание № 1")
doit(chord, function1, left if left else -1., right if right else 1., a)
doit(secant, function1, left if left else -1., right if right else 1., a)
doit(bisection, function1, left if left else -3., right if right else 2., a)
doit(newton, function1, derivative1, start, a)

# Task 2

x0, y0 = 0.5, 0.5
print("Задание № 2")
doit(bfgs, function2, gradient2, x0, y0)
doit(gradient_descent, function2, gradient2, x0, y0)
doit(newton2d, function2, gradient2, hessian2, x0, y0)
doit(conjugate_gradient, function2, gradient2, x0, y0)

# Task 3

print("Задание № 3")

# Task 4

print("Задание № 4")

# Task 5

print("Задание № 5")

# Task 6

print("Задание № 6")

# Task 7

print("Задание № 7")
