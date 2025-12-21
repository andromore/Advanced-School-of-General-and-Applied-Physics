import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def f(x, y):
    return (y - x*np.exp(x))**2 + np.cosh(x*y)

def df(x, y):
    dx = 2*(y - x*np.exp(x))*(-np.exp(x)-x*np.exp(x)) + np.sinh(x*y)*y
    dy = 2*(y - x*np.exp(x)) + np.sinh(x*y)*x
    return np.array([dx, dy])

#1сопряженные градиенты
def cg_opt(f, df, x0, y0, max_iter=100):
    x, y = x0, y0
    g = df(x, y)
    d = -g
    path = [(x, y, f(x, y))]
    
    for _ in range(max_iter):
        res = minimize(lambda a: f(x + a*d[0], y + a*d[1]), 0.1)
        a = res.x[0]
        
        x_new = x + a*d[0]
        y_new = y + a*d[1]
        g_new = df(x_new, y_new)
        path.append((x_new, y_new, f(x_new, y_new)))
        
        if np.linalg.norm(g_new) < 1e-6:
            break
            
        b = np.dot(g_new, g_new)/np.dot(g, g)
        d = -g_new + b*d
        x, y, g = x_new, y_new, g_new
    
    return x, y, np.array(path)

#2градиентный спуск
def gd_opt(f, df, x0, y0, lr=0.01, max_iter=1000):
    path = [(x0, y0, f(x0, y0))]
    for _ in range(max_iter):
        g = df(x0, y0)
        x1 = x0 - lr*g[0]
        y1 = y0 - lr*g[1]
        path.append((x1, y1, f(x1, y1)))
        if np.linalg.norm([x1-x0, y1-y0]) < 1e-6:
            break
        x0, y0 = x1, y1
    return x0, y0, np.array(path)

#переменная метрика
def bfgs_opt(f, df, x0, y0, max_iter=1000):
    res = minimize(lambda p: f(p[0], p[1]), 
                  [x0, y0], 
                  method='BFGS',
                  jac=lambda p: df(p[0], p[1]),
                  options={'maxiter': max_iter})
    path = np.array([(x0, y0, f(x0, y0)), (res.x[0], res.x[1], f(res.x[0], res.x[1]))])
    return res.x[0], res.x[1], path

def plot_opt(path1, path2, path3):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    x = y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    ax1.contourf(X, Y, Z, levels=50, cmap='viridis')
    ax1.plot(path1[:,0], path1[:,1], 'b.', label='CG')
    ax1.plot(path2[:,0], path2[:,1], 'r.', label='GD')
    ax1.plot(path3[:,0], path3[:,1], 'g.', label='BFGS')
    ax1.set_title('траектории')
    
    # Сходимость
    ax2.plot(path1[:,2], 'b-', label='CG')
    ax2.plot(path2[:,2], 'r-', label='GD')
    ax2.plot(path3[:,2], 'g-', label='BFGS')
    ax2.set_title('сходимость')
    ax2.set_yscale('log')
    
    plt.legend()
    plt.show()

x0, y0 = 0.5, 0.5

x1, y1, p1 = cg_opt(f, df, x0, y0)
x2, y2, p2 = gd_opt(f, df, x0, y0)
x3, y3, p3 = bfgs_opt(f, df, x0, y0)

print(f"CG: x={x1:.6f}, y={y1:.6f}, f={f(x1,y1):.6f}")
print(f"GD: x={x2:.6f}, y={y2:.6f}, f={f(x2,y2):.6f}")
print(f"BFGS: x={x3:.6f}, y={y3:.6f}, f={f(x3,y3):.6f}")

plot_opt(p1, p2, p3)