import pandas as pd
import numpy as np
import sys
from scipy.optimize import curve_fit
from scipy.integrate import quad

def gaussian(x, a, mu, sigma):
    return a * np.exp(-(x - mu)**2 / (2 * sigma**2))

def process_excel_gauss_integral(file_path, low_lim, upp_lim):
    try:
        # 1. Чтение данных из столбцов C и D (индексы 2 и 3)
        df = pd.read_excel(file_path, usecols="C:D")
        
        x_raw = pd.to_numeric(df.iloc[:, 0], errors='coerce').values
        y_raw = pd.to_numeric(df.iloc[:, 1], errors='coerce').values

        mask = ~np.isnan(x_raw) & ~np.isnan(y_raw)
        x_clean = x_raw[mask]
        y_clean = y_raw[mask]

        if len(x_clean) < 3:
            print("Ошибка: Недостаточно данных.")
            return

        # 2. Начальное приближение и аппроксимация
        mean_guess = x_clean[np.argmax(y_clean)]
        initial_guess = [np.max(y_clean), mean_guess, np.std(x_clean) / 2]
        
        popt, _ = curve_fit(gaussian, x_clean, y_clean, p0=initial_guess)
        
        # 3. Вычисление интеграла в заданных пределах
        integral_value, _ = quad(gaussian, low_lim, upp_lim, args=tuple(popt))

        # 4. Вывод данных
        print(f"\nФайл: {file_path}")
        print(f"Параметры: A={popt[0]:.4f}, mu={popt[1]:.4f}, sigma={popt[2]:.4f}")
        print(f"Пределы интегрирования: [{low_lim}, {upp_lim}]")
        print(f"Результат: {integral_value:.6f}")

    except Exception as e:
        print(f"Ошибка при обработке: {e}")

if __name__ == "__main__":
    # Проверка наличия аргументов: имя_файла, нижний_предел, верхний_предел
    if len(sys.argv) < 4:
        print("Использование: python script.py <файл> <нижний_предел> <верхний_предел>")
        print("Пример: python 1.py magnetic.xls -5 5")
    else:
        file_arg = sys.argv[1]
        try:
            low_arg = float(sys.argv[2])
            high_arg = float(sys.argv[3])
            process_excel_gauss_integral(file_arg, low_arg, high_arg)
        except ValueError:
            print("Ошибка: Пределы интегрирования должны быть числами.")
