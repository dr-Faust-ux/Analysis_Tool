import requests
import pandas as pd
import matplotlib.pyplot as plt

# Константы
BASE_URL = "https://api.binance.com"
SYMBOL = "BTCUSDT"  # Биткойн к доллару
INTERVAL = "1h"     # Интервал свечей
LIMIT = 100         # Количество последних свечей

def fetch_data(symbol, interval, limit):
    """
    Получает данные о свечах с Binance API.
    """
    endpoint = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Проверка на ошибки
    return response.json()

def process_data(data):
    """
    Преобразует данные свечей в DataFrame.
    """
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = pd.to_numeric(df["close"])
    return df[["timestamp", "close"]]

def plot_data(df):
    """
    Строит график цены и скользящей средней.
    """
    df["SMA"] = df["close"].rolling(window=10).mean()  # Скользящая средняя
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["close"], label="Цена")
    plt.plot(df["timestamp"], df["SMA"], label="Скользящая средняя (SMA)", linestyle="--")
    plt.xlabel("Дата")
    plt.ylabel("Цена (USDT)")
    plt.title("Ценовой график с SMA")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    print("Получение данных...")
    data = fetch_data(SYMBOL, INTERVAL, LIMIT)
    print("Обработка данных...")
    df = process_data(data)
    print("Построение графика...")
    plot_data(df)
    print("Анализ завершен.")

if __name__ == "__main__":
    main()

