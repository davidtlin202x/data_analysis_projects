#Nothing too special here.  Simply plotting the Rank vs Value of top 50 world teams.
#As we can see, Argentina is somewhat overpowered for the low cost of their players!

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('football.csv')

def parse_value(value_string: str):
    if value_string.endswith('bn'):
        return float(value_string[1:-2])*1000
    else:
        return float(value_string[1:-1])

df['value_m'] = df['Team Value'].apply(parse_value)
df['bubble_size'] = (df['Squad Size'] - df['Squad Size'].min())*30 + 40  # Scale bubble size based on squad size
print(df.head())



plt.scatter(df['Rank'], df['value_m'], s=df['bubble_size'], alpha=0.5)
plt.ylabel('Team Value (in millions)')
plt.xlabel('FIFA Rank')
plt.title('FIFA Rank vs Team Value')

#Label points with country names
for i, row in df.iterrows():
    plt.text(row['Rank'], row['value_m'], row['Country'], fontsize=8)

plt.show()
