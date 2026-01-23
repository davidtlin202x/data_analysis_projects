import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


gdf = gpd.read_file("london_boroughs.geojson")

#Show the GDF as a plot
gdf.plot()
# plt.show()

#Read in the London-Borough Profile data
df = pd.read_csv("london-data.csv")

#View the columns and the first few lines of the DataFrame
print(df.head())
print(df.columns)


#Rename the columns to be more managable
#"Anxiety_score_2011-14_(out_of_10)" --> "anxiety"
#"Turnout_at_2014_local_elections" --> "turnout"
#"Childhood_Obesity_Prevalance_(%)_2015/16" --> "child_obesity"
#"Mortality_rate_from_causes_considered_preventable_2012/14" --> "mortality"
df = df.rename(columns={
   "Anxiety_score_2011-14_(out_of_10)": "anxiety",
   "Turnout_at_2014_local_elections": "turnout",
   "Childhood_Obesity_Prevalance_(%)_2015/16": "child_obesity",
   "Mortality_rate_from_causes_considered_preventable_2012/14": "mortality"
})

#Join the DataFrames with the Cleaned Data to the GeoData and set the index to "borough"
merged = gdf.set_index("name").join(df.set_index("borough"))


# Choose columns to plot; for visibility, we limit ourselves to 4
variables_to_plot = ["anxiety", "turnout", "child_obesity", "mortality"]
titles = ["Anxiety Score", "Turnout at 2014 Local Elections", "Childhood Obesity Prevalence", "Mortality Rate from Preventable Causes"]
cmaps = ["OrRd","coolwarm","PiYG","YlGnBu"]

# Make the map
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

for i, variable_to_plot in enumerate(variables_to_plot):
    ax = axes[i // 2, i % 2]
    merged.plot(
        column=variable_to_plot,
        ax=ax,
        cmap=cmaps[i],
        linewidth=0.8,
        edgecolor='0.8',
        legend=True,
    )
    ax.set_title(titles[i])
    
plt.savefig("london_boroughs_analysis.png")
plt.show()



