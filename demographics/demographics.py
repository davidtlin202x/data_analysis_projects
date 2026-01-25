import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math

#Read in data files
df_fertility = pd.read_csv("data/fertility-rate.csv")
df_gdp = pd.read_csv("data/gdp-per-capita.csv")

#View
'''
print(df_fertility.head())
print(df_gdp.head())
'''

#Rename excessively long column name
df_fertility.rename(columns={'Fertility rate - Sex: all - Age: all - Variant: estimates': 'fertility'}, inplace=True)
df_gdp.rename(columns={'GDP per capita, PPP (constant 2021 international $)': 'gdp',
                       'World region according to OWID': 'region'}, inplace=True)


#Check the range of years
'''print(df_fertility['Year'].min(), df_fertility['Year'].max())
print(df_gdp['Year'].min(), df_gdp['Year'].max())
'''

df_fertility = df_fertility[df_fertility['Year'] == 2023].set_index('Entity')
df_gdp = df_gdp[df_gdp['Year'] == 2023].set_index('Entity')
#Since we are only using data from 2023, we can drop the year column
df_fertility.drop(columns=['Year'], inplace=True)
df_gdp.drop(columns=['Year'], inplace=True)

# Merge and drop any row that doesn't have data
merged = df_fertility.join(df_gdp, how='inner', lsuffix='_f', rsuffix='_gdp').dropna()

#Now we can plot the data
# sns.scatterplot(data=merged, x='gdp', y='fertility')

#The preliminary plot looks like it could be logarithmic so let's check this out
# sns.scatterplot(data=merged, x='fertility', y='gdp').set(yscale='log')

#Add a log column to the GDP data, then fit linear regression
merged['log_gdp'] = merged['gdp'].apply(lambda x: math.log(x))
X = merged[['fertility']] #independent variable
y = merged['log_gdp']
model = LinearRegression().fit(X,y)
print(f"m={model.coef_[0]}\nb={model.intercept_}\nR^2={model.score(X,y)}")

#Plot the data with regions
markers = {'Asia': 'o', 'Europe': 'v', 'Africa': 's', 'North America': 'D', 'South America' : 'P', 'Oceania': '*'}
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=merged, x='fertility', y='log_gdp', style='region', hue='region', markers =markers, s=80)
# Show the regression line
x_vals = [i/2 for i in range(1, 13)]
y_vals = model.predict([[x] for x in x_vals])
plt.plot(x_vals, y_vals, color='black', linestyle='--')
plt.savefig("result.png", dpi=300)
plt.show()