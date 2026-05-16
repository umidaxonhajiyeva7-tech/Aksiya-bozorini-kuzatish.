import yfinance as yf
import pandas as pd
import pyodbc
from datetime import datetime

# 1. AKSIYA MA'LUMOTLARINI YUKLAB OLISH (AAPL va MSFT)
tickers = ['AAPL', 'MSFT']
bugun = datetime.today().strftime('%Y-%m-%d')

print("Aksiya ma'lumotlari yuklanmoqda...")
data = yf.download(tickers, period='1d')

kotirovka = []
for ticker in tickers:
    yopilish_narxi = float(data['Close'][ticker].iloc[-1])
    ochilish_narxi = float(data['Open'][ticker].iloc[-1])
    ozgarish_foiz = ((yopilish_narxi - ochilish_narxi) / ochilish_narxi) * 100
    
    kotirovka.append({
        'Sana': bugun,
        'Kompaniya': ticker,
        'Ochilish': round(ochilish_narxi, 2),
        'Yopilish': round(yopilish_narxi, 2),
        'Ozgarish_Foiz': round(ozgarish_foiz, 2)
    })

# Pandas DataFrame orqali tahlil qilish
df = pd.DataFrame(kotirovka)
print("\nPandas DataFrame Natijasi:")
print(df)

# 2. AZURE SQL BAZASIGA ULASH VA YOZISH
# (Bu yerga o'z Azure SQL ma'lumotlaringizni yozasiz)
server = 'your_server.database.windows.net'
database = 'your_database'
username = 'your_username'
password = 'your_password'
driver= '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Jadvalni tekshirish va yaratish
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AksiyaTahlili' AND xtype='U')
        CREATE TABLE AksiyaTahlili (
            Sana DATE,
            Kompaniya VARCHAR(10),
            Ochilish FLOAT,
            Yopilish FLOAT,
            Ozgarish_Foiz FLOAT
        )
    ''')
    conn.commit()

    # Ma'lumotlarni yozish
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO AksiyaTahlili (Sana, Kompaniya, Ochilish, Yopilish, Ozgarish_Foiz)
            VALUES (?, ?, ?, ?, ?)
        ''', row['Sana'], row['Kompaniya'], row['Ochilish'], row['Yopilish'], row['Ozgarish_Foiz'])
    
    conn.commit()
    print("\nMa'lumotlar Azure SQL-ga muvaffaqiyatli yozildi!")

except Exception as e:
    print("\nXatolik:", e)
finally:
    if 'conn' in locals():
        conn.close()
    
