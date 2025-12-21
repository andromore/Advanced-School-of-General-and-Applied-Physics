# -*- coding: utf-8 -*-
"""
Программа для решения уравнения F(x,a) = sin(x)/x^2 - a = 0 
методом Ньютона с последующей интерполяцией и аппроксимацией
"""

import numpy as np
import matplotlib.pyplot as plt

def F(x, a):
    """Целевая функция F(x,a) = sin(x)/x^2 - a"""
    return np.sin(x)/x**2 - a  

def F1(x, a):
    """Первая производная F по x (аналитически вычисленная)"""
    return np.cos(x)/x**2 - 2*np.sin(x)/(x**3)
    
def newton(a):
    """
    Реализация метода Ньютона для нахождения корня F(x,a)=0
    Args:
        a: параметр уравнения
    Returns:
        Найденный корень x
    """
    # Начальные границы и приближение
    b = 0  # левая граница (не используется, можно удалить)
    c = 1  # правая граница (не используется, можно удалить)
    delta = 1e-5  # критерий остановки
    
    x0 = 0.5  # начальное приближение (можно улучшить)
    xn = F(x0, a)
    
    # Итерационный процесс Ньютона
    xn1 = xn - F(xn, a)/F1(xn, a)
    while abs(xn1 - xn) > delta:
        xn = xn1    
        xn1 = xn - F(xn, a)/F1(xn, a)
    return xn1

# Пример использования
print('Корень при а=1:', newton(1))

def der_Newton(h, a):
    """Численное вычисление производной dx/da методом центральных разностей"""
    return (newton(a + h) - newton(a - h))/(2*h)

print('Производная в а=1:', der_Newton(0.001, 1))

def second_der_Newton(h, a):
    """Численное вычисление второй производной d²x/da²"""
    return (newton(a + h) - 2*newton(a) + newton(a - h))/(h**2)

# Создание массива значений параметра a
arg_a = np.linspace(0.1, 2, 20)  # лучше избегать a=0 из-за деления на 0
res = np.array([newton(a) for a in arg_a])  # вычисление корней для всех a

# Визуализация зависимости корня от параметра
plt.figure(figsize=(10, 6))
plt.plot(arg_a, res)
plt.title("Зависимость корня x от параметра a")
plt.xlabel("a")
plt.ylabel("x")
plt.grid()
plt.show()

def Rational(a):
    """Рациональная интерполяция зависимости x(a)"""
    # Опорные точки для интерполяции
    points = [0, 4, 8, 12, 16]  # индексы контрольных точек
    
    # Значения функции в опорных точках
    z = [res[i] for i in points]
    a_vals = [arg_a[i] for i in points]
    
    # Вычисление обратных разностей
    # (здесь можно реализовать более аккуратный алгоритм)
    z01 = (a_vals[0] - a_vals[1])/(z[0] - z[1])
    # ... остальные разности вычисляются аналогично
    
    # Рекурсивная формула рациональной интерполяции
    return z[0] + (a - a_vals[0])/(z01 + (a - a_vals[1])/(...))

# Аппроксимация Паде (2-го порядка)
def Pade(a):
    """Аппроксимация Паде зависимости x(a)"""
    a0 = arg_a[8]  # точка разложения
    x0 = newton(a0)
    dx = der_Newton(0.01, a0)
    d2x = second_der_Newton(0.01, a0)
    
    # Коэффициенты аппроксимации
    A = x0*d2x - 2*dx**2
    B = -2*x0*dx
    C = d2x
    D = -2*dx
    
    return (A*(a - a0) + B)/(C*(a - a0) + D)

# Численное интегрирование
def trapezoid_method(a):
    """Вычисление интеграла от Rational(a) методом трапеций"""
    n = 20
    a_left = 0.1  # нижний предел интегрирования
    h = (a - a_left)/n
    
    integral = 0.5*(Rational(a_left) + Rational(a))
    for i in range(1, n):
        integral += Rational(a_left + i*h)
    return integral * h