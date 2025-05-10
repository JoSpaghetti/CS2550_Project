import folium
from folium.plugins import LocateControl
from database.database import LocationDatabase #local database

"""
database return structure:
[("Name", "LocationType", "Latitude", "Longitude", "Address", "City", "State", "Country", "ZipCode"),]
"""

def new_map(longitude, latitude):
    # Load the database file
    local_db = LocationDatabase("database/")
    print ("Database Initialized")

    # get a list of locations near a point
    nearby_locations = local_db.nearby_locations(longitude1=longitude,
                                                 latitude1=latitude,
                                                 distance_range=75,
                                                 units="mi",
                                                 )
    print ("Nearby Locations Generated")

    # Create a basic map centered at the location parameters passed into the method
    latitude = nearby_locations[0][2]
    longitude = nearby_locations[0][3]
    gps_map = folium.Map(location=[latitude, longitude],
                         zoom_start=12,
                         control_scale=True)

    # Add a locator button to the map
    folium.plugins.LocateControl(auto_click=True,
                                 flyTo=True,
                                 ).add_to(gps_map)

    print ("Basic Map Generated")

    # Add markers for each restaurant
    locations = []
    for location in nearby_locations:
        text = f"{location[0]}:\n {location[4]}, {location[5]}, {location[6]}, {location[7]}, {location[8]} "
        folium.Marker(
            location=[location[2], location[3]],
            tooltip=location[1],
            popup=text,
            max_width=200
        ).add_to(gps_map)
        locations.append(location)

    print ("Location Markers Placed")

    # Add the dropdown and script to the map
    # gps_map.get_root().html.add_child(folium.Element(dropdown_html + dropdown_script))

    # Save the map to an HTML file
    filename = 'gps_map.html'
    gps_map.save(filename)

    print(f"Map has been created and saved as {filename}.")

if __name__ == "__main__":
    new_map(-117.821667, 34.056389)

