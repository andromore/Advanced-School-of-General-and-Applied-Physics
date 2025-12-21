import numpy as np

def f(x, a):
    return a * x - 1 / np.tan(x)  

def find_x(a, eps=1e-8):
    x = 0.9  
    for _ in range(100):
        fx = f(x, a)
        dfx = a + 1/(np.sin(x)**2)  
        
        if abs(dfx) < 1e-12:
            break
            
        delta = fx / dfx
        x -= delta
        
        if abs(delta) < eps:
            break
    return x

#метод Рунге-Ромберга
def rr_method(a_vals):
    roots = []
    for a in a_vals:
        root = find_x(a, eps=1e-8)
        roots.append(root)
    
    h = a_vals[1] - a_vals[0]  
    idx = np.argmin(np.abs(np.array(a_vals) - 1.0))  
    dxda = (-roots[idx+2] + 8*roots[idx+1] - 8*roots[idx-1] + roots[idx-2]) / (12 * h)
    return roots, dxda

#полиномиальная аппроксимация
def poly_method(a_vals, roots):
    n = len(a_vals)
    V = np.zeros((n, 3))
    for i in range(n):
        V[i][0] = a_vals[i]**2
        V[i][1] = a_vals[i]
        V[i][2] = 1
    
    VT = V.T
    A = VT @ V
    b = VT @ roots
    coef = np.linalg.solve(A, b)
    
    deriv = [2*coef[0], coef[1]]
    dxda = deriv[0] * 1.0 + deriv[1]
    
    return dxda, coef

#метод регуляризации
def reg_method(a_vals, roots):
    a_target = 1.0 
    idx = np.argmin(np.abs(np.array(a_vals) - a_target))
    window = slice(max(0, idx-2), min(len(a_vals), idx+3))
    
    a_win = np.array(a_vals)[window]
    x_win = np.array(roots)[window]
    
    a_mean = np.mean(a_win)
    x_mean = np.mean(x_win)
    
    Sxy = np.sum((a_win - a_mean) * (x_win - x_mean))
    Sxx = np.sum((a_win - a_mean)**2)
    
    return Sxy / Sxx


a_vals = [0.9 + 0.01*i for i in range(21)]  
roots, dxda_rr = rr_method(a_vals)
print(f"Рунге-Ромберг: dx*/da a=1 {dxda_rr:.6f}")

dxda_poly, coef = poly_method(a_vals, roots)
print(f"Полиномиальная:\ndx*/da a=1 {dxda_poly:.8f}")
print(f"Коэффициенты: {coef}")

dxda_reg = reg_method(a_vals, roots)
print(f"Регуляризация:\ndx*/da a=1  {dxda_reg:.8f}")

estimates = [dxda_rr, dxda_poly, dxda_reg]
max_diff = max(estimates) - min(estimates)
print(f"\nМаксимальная разница: {max_diff:.2e}")