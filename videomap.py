import pandas as pd
import folium
from folium.plugins import LocateControl

# Load the CSV file
file = pd.read_csv('Fast_Food_Restaurants_US.csv')

# Create a basic map centered at the first location in the dataset
latitude = file['latitude'].iloc[0]
longitude = file['longitude'].iloc[0]
map = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add markers for each restaurant
locations = []
for index, row in file.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row.get('name', 'Fast Food Restaurant')  # Replace 'categories' with the actual column for names
    ).add_to(map)
    locations.append((row.get('name', 'Fast Food Restaurant'), row['latitude'], row['longitude']))

# Add a locator button to the map
LocateControl().add_to(map)


# Add the dropdown and script to the map
map.get_root().html.add_child(folium.Element(dropdown_html + dropdown_script))

# Save the map to an HTML file
map.save('fast_food_map.html')

print("Map has been created and saved as 'fast_food_map.html'.")