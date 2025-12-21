# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:58:02 2022

@author: 425
"""
import numpy as np
import matplotlib.pyplot as plt

def F(x, a):
    return np.sin(x)/x**2 - a  # Описание функции

def F1(x, a):
    return np.cos(x)/x**2 - 2*np.sin(x)/(x**3)  # Производная функции
    
def newton(a):  # Метод Ньютона для нахождения корня
    b = 0
    c = 1
    delta = 1e-5  # Точность
    x0 = (c + b)/2
    xn = F(x0, a)
    xn1 = xn - F(xn, a)/F1(xn, a)  # xn1 - следующая итерация
    while abs(xn1 - xn) > delta:
        xn = xn1    
        xn1 = xn - F(xn, a)/F1(xn, a)
    return xn1

print('Корень уравнения при а=1:', newton(1))    
      
def der_Newton(h, a):  # Производная методом симметричной разностной схемы
    Fx = (newton(a + h) - newton(a - h))/(2*h)
    return Fx

print('Производная в а=1:', der_Newton(0.001, 1))

def second_der_Newton(h, a):  # Вторая производная
    Fxx = (newton(a + h) - 2*newton(a) + newton(a - h))/(h**2)
    return Fxx

# Построение графика корня в зависимости от параметра a
arg_a = np.arange(0, 2, 0.1)
res = np.zeros(20)
for i in range(20):
    res[i] = newton(arg_a[i])
    
fig, ax = plt.subplots()    
plt.title("График корня")
plt.xlabel("a") 
plt.ylabel("x (корень)") 
plt.grid()      
plt.plot(arg_a, res)  

def Rational(a):  # Рациональная интерполяция
    # Выбираем опорные точки
    z0 = res[0]
    z1 = res[4]
    z2 = res[8]
    z3 = res[12]
    z4 = res[16]
     
    # Вычисляем обратные разности
    z01 = (arg_a[0] - arg_a[4])/(z0 - z1)
    z02 = (arg_a[0] - arg_a[8])/(z0 - z2)
    z03 = (arg_a[0] - arg_a[12])/(z0 - z3)
    z04 = (arg_a[0] - arg_a[16])/(z0 - z4)
    z012 = (arg_a[4] - arg_a[8])/(z01 - z02)
    z013 = (arg_a[4] - arg_a[12])/(z01 - z03)
    z014 = (arg_a[4] - arg_a[16])/(z01 - z04)
    z0123 = (arg_a[8] - arg_a[12])/(z012 - z013)
    z0124 = (arg_a[8] - arg_a[16])/(z012 - z014)
    z01234 = (arg_a[12] - arg_a[16])/(z0123 - z0124)
    
    # Формула рациональной интерполяции
    return z0 + (a - arg_a[0])/(z01 + (a - arg_a[4])/(z012 + (a - arg_a[8])/(z0123 + (a - arg_a[12])/(z01234 + (a - arg_a[16])))))

# Сравнение интерполяции с исходными данными
x2 = Rational(arg_a)      
x1 = res
fig, ax = plt.subplots()    
plt.title("Интерполяция рациональной функцией")
plt.xlabel("a") 
plt.ylabel("x (корень)") 
plt.grid()      
plt.plot(arg_a, x2, label='Интерполированный график')        
plt.plot(arg_a, x1, label='Исходный график')  
plt.legend()  

def Pade(a):  # Аппроксимация Паде
    a0 = arg_a[8]
    A = newton(a0)*second_der_Newton(0.01, a0) - 2*(der_Newton(0.01, a0)**2)
    B = -2*newton(a0)*der_Newton(0.01, a0)
    C = second_der_Newton(0.01, a0)
    D = -2*der_Newton(0.01, a0)
    return (A*(a - a0) + B)/(C*(a - a0) + D)

x2 = Pade(arg_a)      
x1 = res
fig, ax = plt.subplots()    
plt.title("Аппроксимация Паде")
plt.xlabel("a") 
plt.ylabel("x (корень)") 
plt.grid()      
plt.plot(arg_a, x2, label='Аппроксимированный график')        
plt.plot(arg_a, x1, label='Исходный график')  
plt.legend()

def trapezia_method(a):  # Метод трапеций для вычисления интеграла
    n = 20
    a_left = 0  # Левый конец интервала
    da = (a - a_left)/n
    sum = 0.5 * (Rational(a_left) + Rational(a))  # Формула трапеций
    for i in range(1, n + 1):
        sum += Rational(a_left + i * da)
    return sum * da
 
arg_a = np.arange(0, 2, 0.1)  # Строим график первообразной
y1 = trapezia_method(arg_a)    
fig, ax = plt.subplots()    
plt.title("Первообразная")
plt.xlabel("a") 
plt.ylabel("y") 
plt.grid()      
plt.plot(arg_a, y1)  

plt.show()