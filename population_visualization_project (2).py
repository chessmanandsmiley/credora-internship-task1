
# 🌍 Population Data Visualization Project
# Submitted by: Alamuru Venkata Harshitha
# Internship Task – Credora

# 📦 Import Required Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 📥 Load the Population and Metadata CSV Files
population_df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_85220.csv', skiprows=4)
metadata_df = pd.read_csv('Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_85220.csv')

# 🧹 Clean and Transform Population Data
population_df = population_df.drop(['Indicator Name', 'Indicator Code'], axis=1)
df_long = population_df.melt(id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='Population')
df_long['Year'] = df_long['Year'].astype(int)
merged_df = df_long.merge(metadata_df[['Country Code', 'Region', 'IncomeGroup']], on='Country Code', how='left')
merged_df = merged_df.dropna(subset=['Population'])

# 📊 Bar Chart - Population by Region (Latest Year)
latest_year = merged_df['Year'].max()
region_pop = merged_df[merged_df['Year'] == latest_year].groupby('Region')['Population'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,6))
sns.barplot(x=region_pop.values, y=region_pop.index)
plt.title(f'Total Population by Region ({latest_year})')
plt.xlabel('Population')
plt.ylabel('Region')
plt.tight_layout()
plt.show()

# 📈 Line Chart - Population Growth Over Time
selected_countries = ['India', 'China', 'United States', 'Brazil', 'Nigeria']
plt.figure(figsize=(12,6))
for country in selected_countries:
    data = merged_df[merged_df['Country Name'] == country]
    plt.plot(data['Year'], data['Population'], label=country)
plt.legend()
plt.title('Population Growth Over Time')
plt.xlabel('Year')
plt.ylabel('Population')
plt.tight_layout()
plt.show()

# 🌐 Choropleth Map - Population by Country (Latest Year)
choropleth_df = merged_df[merged_df['Year'] == latest_year]
fig = px.choropleth(
    choropleth_df,
    locations='Country Code',
    color='Population',
    hover_name='Country Name',
    color_continuous_scale='Viridis',
    title=f'World Population by Country ({latest_year})'
)
fig.show()
