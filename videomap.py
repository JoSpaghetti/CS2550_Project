import folium
from folium.plugins import LocateControl
from database.database import LocationDatabase #local database

"""
database return structure:
[("Name", "LocationType", "Latitude", "Longitude", "Address", "City", "State", "Country", "ZipCode", "Location_ID", ),]
"""
def distance_map(location1, location2):
    # Load the database file
    local_db = LocationDatabase("database/")
    print ("Database Initialized")

    # get a list of locations near a point
    location_1 = local_db.location_search(location_id = location1)
    location_2 = local_db.location_search(location_id = location2)
    nearby_locations = location_1 + location_2

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
    coord_points = []
    for location in nearby_locations:
        text = f"{location[0]}-{location[9]}:\n {location[4]}, {location[5]}, {location[6]}, {location[7]}, {location[8]} "
        folium.Marker(
            location=[location[2], location[3]],
            tooltip=location[1],
            popup=text,
            max_width=200
        ).add_to(gps_map)
        locations.append(location)

        coord_points.append([ location[2], location[3] ])

    print (coord_points)

    dist_between = LocationDatabase.distance_between(longitude1=coord_points[0][0],
                                                     latitude1= coord_points[0][1],
                                                     longitude2= coord_points[2][0],
                                                     latitude2= coord_points[2][1],
                                                     units = "km")

    folium.plugins.AntPath(
        locations=coord_points,
        tooltip=f"{dist_between:.2f} km",
        popup=f"Total Distance: {dist_between:.2f} km",
        reverse=True,
        dath_array=[20,30]
    ).add_to(gps_map)

    print ("Location Markers Placed")

    # Add the dropdown and script to the map
    # gps_map.get_root().html.add_child(folium.Element(dropdown_html + dropdown_script))

    # Save the map to an HTML file
    filename = 'gps_map.html'
    gps_map.save(filename)

    print(f"Map has been created and saved as {filename}.")

def search_map(name, address, city, state, zipcode):
    # Load the database file
    local_db = LocationDatabase("database/")
    print ("Database Initialized")

    # get a list of locations near a point
    nearby_locations = local_db.location_search(name=name, address=address, city=city, state=state, zipcode=zipcode)

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
        text = f"{location[0]}-{location[9]}:\n {location[4]}, {location[5]}, {location[6]}, {location[7]}, {location[8]} "
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

def nearby_location_map(latitude, longitude, dist_range, units ):
    # Load the database file
    local_db = LocationDatabase("database/")
    print ("Database Initialized")

    # get a list of locations near a point
    nearby_locations = local_db.nearby_locations(longitude1=longitude,
                                                 latitude1=latitude,
                                                 distance_range=dist_range,
                                                 units=units,
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
        text = f"{location[0]}-{location[9]}:\n {location[4]}, {location[5]}, {location[6]}, {location[7]}, {location[8]} "
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
    nearby_location_map(-117.821667, 34.056389, 100, "mi")


