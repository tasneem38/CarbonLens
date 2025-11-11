import numpy as np

def naive_forecast_series(base_month_kg: float, months: int = 6):
    # simple sinusoidal fluctuation to demo trend
    return [round(base_month_kg + 40*np.sin(i/2), 1) for i in range(months)]
