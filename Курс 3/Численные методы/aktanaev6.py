import time
import matplotlib.pyplot as plt
import numpy as np

# постановка нашей задачи
x0 = 0
x_end = 10.0  
y0 = 0.0      
yp0 = 1.0     
h = 0.01     

def derivatives(u, y):
    dy = u
    du = -np.sin(y)
    return dy, du

def stormer_acceleration(y, dy):
    return -np.sin(y)

#Рунге-кутта
def runge_kutta(x0, x_end, y0, yp0, h):
    x = [x0]
    y = [y0]
    u = [yp0]
    max_steps = int((x_end - x0) / h) + 1
    
    for step in range(max_steps):
        if x[-1] >= x_end:
            break
        
        current_u = u[-1]
        current_y = y[-1]
        
        try:
            k1_y, k1_u = derivatives(current_u, current_y)
            k2_y, k2_u = derivatives(current_u + 0.5*h*k1_u, current_y + 0.5*h*k1_y)
            k3_y, k3_u = derivatives(current_u + 0.5*h*k2_u, current_y + 0.5*h*k2_y)
            k4_y, k4_u = derivatives(current_u + h*k3_u, current_y + h*k3_y)
        except OverflowError:
            print(f"переполнение шаг {step}. последние значения: y={current_y}, u={current_u}")
            break
        
        new_y = current_y + (k1_y + 2*k2_y + 2*k3_y + k4_y) * h / 6
        new_u = current_u + (k1_u + 2*k2_u + 2*k3_u + k4_u) * h / 6
        new_x = x[-1] + h
        
        if not (abs(new_y) < 1e100 and abs(new_u) < 1e100):
            print(f"аномальные значения на шаге {step}. остановка")
            break
        
        x.append(new_x)
        y.append(new_y)
        u.append(new_u)
    
    return x, y

# Штермер
def stormer(x0, x_end, y0, yp0, h):
    x = [x0]
    y = [y0]
    
    # 1 шаг метод Эйлера
    if len(x) < 2:
        dy = yp0
        y_next = y[0] + dy*h + 0.5*h**2*stormer_acceleration(y[0], dy)
        x.append(x[0] + h)
        y.append(y_next)
    
    while x[-1] < x_end:
        acceleration = stormer_acceleration(y[-1], (y[-1]-y[-2])/h)
        try:
            y_next = 2 * y[-1] - y[-2] + h**2 * acceleration
            x_next = x[-1] + h

            if abs(x_next) > 1e100 or abs(y_next) > 1e100:
                raise OverflowError("аномальный рост решения")

        except OverflowError as e:
            print(f"\033[31mошибка: {e}. остановка\033[0m")
            break
        except Exception as e:
            print(f"\033[31mнепредвиденная ошибка: {e}\033[0m")
            break
        else:
            y.append(y_next)
            x.append(x_next)
    return x, y

# Адамс
def adams(x0, x_end, y0, yp0, h):
    x = [x0]
    y = [y0]
    u = [yp0] 
    
    #4 точки методом Р-к
    for _ in range(3):
        current_u = u[-1]
        current_y = y[-1]
        k1_y, k1_u = derivatives(current_u, current_y)
        k2_y, k2_u = derivatives(current_u + 0.5*h*k1_u, current_y + 0.5*h*k1_y)
        k3_y, k3_u = derivatives(current_u + 0.5*h*k2_u, current_y + 0.5*h*k2_y)
        k4_y, k4_u = derivatives(current_u + h*k3_u, current_y + h*k3_y)
        
        new_y = current_y + (k1_y + 2*k2_y + 2*k3_y + k4_y) * h / 6
        new_u = current_u + (k1_u + 2*k2_u + 2*k3_u + k4_u) * h / 6
        new_x = x[-1] + h
        
        x.append(new_x)
        y.append(new_y)
        u.append(new_u)
        
    while x[-1] < x_end:
        du_current = derivatives(u[-1], y[-1])[1]
        du_prev1 = derivatives(u[-2], y[-2])[1]
        du_prev2 = derivatives(u[-3], y[-3])[1]
        du_prev3 = derivatives(u[-4], y[-4])[1]
        
        new_u = u[-1] + h/24 * (55 * du_current - 59 * du_prev1 + 37 * du_prev2 - 9 * du_prev3)
        new_y = y[-1] + h/24 * (55 * u[-1] - 59 * u[-2] + 37 * u[-3] - 9 * u[-4])
        new_x = x[-1] + h
        
        x.append(new_x)
        y.append(new_y)
        u.append(new_u)
    
    return x, y

#вычисление и сравнение результатов
def solve_and_compare():
    start = time.time()
    x_rk, y_rk = runge_kutta(x0, x_end, y0, yp0, h)
    time_rk = time.time() - start
    
    start = time.time()
    x_st, y_st = stormer(x0, x_end, y0, yp0, h)
    time_st = time.time() - start
    
    start = time.time()
    x_ad, y_ad = adams(x0, x_end, y0, yp0, h)
    time_ad = time.time() - start
    
    print("\nРезультаты:")
    print(f"Метод Рунге-Кутта: {time_rk:.4f} с, точек: {len(x_rk)}")
    print(f"Метод Штермера:  {time_st:.4f} с, точек: {len(x_st)}")
    print(f"Метод Адамса: {time_ad:.4f} с, точек: {len(x_ad)}")
    
    #сравнение в конечной точке
    print("\nСравнение в конечной точке x =", x_end)
    print(f"Рунге-Кутта: y({x_end}) = {y_rk[-1]:.6f}")
    print(f"Штермер: y({x_end}) = {y_st[-1]:.6f}")
    print(f"Адамс: y({x_end}) = {y_ad[-1]:.6f}")
    
    #разница между методами
    diff_rk_st = abs(y_rk[-1] - y_st[-1])
    diff_rk_ad = abs(y_rk[-1] - y_ad[-1])
    diff_st_ad = abs(y_st[-1] - y_ad[-1])
    
    print("\nРазница между методами:")
    print(f"Рунге-Кутта; Штермер: {diff_rk_st:.2e}")
    print(f"Рунге-Кутта; Адамс: {diff_rk_ad:.2e}")
    print(f"Штермер; Адамс:   {diff_st_ad:.2e}")
    
    plt.figure(figsize=(12, 6))
    plt.plot(x_rk, y_rk, 'b-', lw=1, label='Рунге-Кутта')
    plt.plot(x_st, y_st, 'r--', lw=1, label='Штермер')
    plt.plot(x_ad, y_ad, 'g-.', lw=1, label='Адамс')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y(x)', fontsize=12)
    plt.title('Решение уравнения y\'\' + sin(y) = 0', fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=10)
    plt.show()
    
if __name__ == "__main__":
    solve_and_compare()