import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Kun": ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma"],
    "Narx": [120, 125, 123, 130, 128]
}

df = pd.DataFrame(data)

print(df)

plt.plot(df["Kun"], df["Narx"], marker='o')

plt.title("Aksiya bozori")
plt.xlabel("Kun")
plt.ylabel("Narx")

plt.show()
