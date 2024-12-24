import requests 
from datetime import datetime
import tkinter as tk
from tkinter import ttk

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric", 
        "lang": "ja"      
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        weather_data = response.json()
        
        weather_info = {
            "都市": weather_data["name"],
            "気温": f"{weather_data['main']['temp']}°C",
            "最高気温": f"{weather_data['main']['temp_max']}°C", 
            "最低気温": f"{weather_data['main']['temp_min']}°C",
            "湿度": f"{weather_data['main']['humidity']}%",
            "天気": weather_data["weather"][0]["description"],
            "取得時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather_info
    
    except requests.exceptions.RequestException as e:
        return f"エラーが発生しました: {e}"

def search_weather():
    city = city_entry.get()
    if not city:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "都市名を入力してください")
        return
        
    weather_info = get_weather(city, API_KEY)
    result_text.delete(1.0, tk.END)
    
    if isinstance(weather_info, dict):
        output = "=== 天気情報 ===\n"
        for key, value in weather_info.items():
            output += f"{key}/ {value}\n"
        result_text.insert(tk.END, output)
    else:
        result_text.insert(tk.END, weather_info)

def main():
    global city_entry, result_text, API_KEY
    API_KEY = "39bb662c5ab078ba16a0f8ef2cf8bf65"
    
    root = tk.Tk()
    root.title("天気情報アプリ")
    
    frame = ttk.Frame(root, padding="10")
    frame.pack(expand=True, fill="both")
    
    input_frame = ttk.Frame(frame)
    input_frame.pack(fill="x", padx=5, pady=5)
    
    ttk.Label(input_frame, text="都市名:").pack(side="left")
    city_entry = ttk.Entry(input_frame)
    city_entry.pack(side="left", padx=5)
    ttk.Button(input_frame, text="天気を検索", command=search_weather).pack(side="left")
    
    result_text = tk.Text(frame, height=10, width=40)
    result_text.pack(expand=True, fill="both", pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    import os
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')
    main()