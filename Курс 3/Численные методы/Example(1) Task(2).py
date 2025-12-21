# -*- coding: utf-8 -*-
"""
Created on Tue May 17 19:12:12 2022

@author: 425
"""

import numpy as np

def F(x, y):
    """Функция для оптимизации"""
    if x > 0:  
        return (y/x - np.log(x))**2 + np.exp(y**2)
    else:
        return 'Точка находится вне области определения'      
        
def grad_F(x, y):
    """Градиент функции F"""
    gF = np.zeros((2, 1))
    a = 2 * (y / x - np.log(x)) / x
    gF[0] = a * (-y/x - 1)
    gF[1] = a + 2*y*np.exp(y**2)
    return gF

x0, y0 = list(map(float, input("Начальная точка (введите через пробел): x0, y0 = ").split()))

def Spusk(delta):
    """Метод градиентного спуска"""
    gF = grad_F(x0, y0)
    
    while np.linalg.norm(gF) > delta:
        # Нормируем градиент и задаем шаг вдоль него
        norm_grad_F = gF / np.linalg.norm(gF)
        lamda = 0.0001
        
        x = x0 - lamda * norm_grad_F[0]
        y = y0 - lamda * norm_grad_F[1]
        
        # Условие минимума и описание метода
        while F(x, y) > F(x - lamda * norm_grad_F[0], y - lamda * norm_grad_F[1]):
            gF = grad_F(x, y)
            norm_grad_F = gF / np.linalg.norm(gF)
            lamda = lamda
            x = x - lamda * norm_grad_F[0]
            y = y - lamda * norm_grad_F[1]
                    
        return (x, y, F(x, y))

if x0 > 0:
    print('Минимум находится в точке и его значение:', Spusk(10**-5))
else: 
    print('Невозможно посчитать значение - точка лежит вне области определения')