import pandas as pd
import duckdb
import geopy
from geopy import distance

class LocationDatabase:
    connection = duckdb.connect(':memory:')
    df_name = "locations_df"
    database_name = "location_table"

    def __init__(self, folder=""):
        self.folder = folder
        museum = self.__start_museums_aquarium_zoo_dataframe()
        fast_food = self.__fast_food_restaurant_dataframe()
        hospital = self.__us_hospital_locations_dataframe()

        #dataframe for all location types
        locations_df = pd.concat([museum, fast_food, hospital], ignore_index=True, sort=False)

        locations_df["Location_ID"] = locations_df.index

        #print(locations_df)

        #referenced from DuckDB documentation and https://medium.com/@anshubantra/using-duckdb-in-python-a-comprehensive-guide-d14bc0b06546

        #create table
        self.connection.sql(f"CREATE OR REPLACE TABLE {self.database_name} AS SELECT * FROM {self.df_name}")

        #insert elements into table
        self.connection.sql(f'INSERT INTO {self.database_name} SELECT * FROM {self.df_name}')


    def nearby_locations(self, longitude1, latitude1, distance_range, units="km"):
        """Given a set of coordinate values and a distance, it returns a series of location values
        :param longitude1: Longitude of first location
        :param latitude1: Latitude of first location
        :param distance_range: Range of distance in meters
        :param units: the unit of distance measure"""

        #if one set of longitude and a distance are given
        start_point = (latitude1, longitude1)
        bounding_box = dict()
        for degree in [0,90,180,270]:
            if units == "mi":
                distance_length = geopy.distance.distance(miles = distance_range/2).destination(point = start_point,
                                                                                                bearing=degree)
                bounding_box[degree] = distance_length


            if units == "km":
                distance_length = geopy.distance.distance(kilometers=distance_range/2).destination(point=start_point,
                                                                                                   bearing=degree)
                bounding_box[degree] = distance_length

        #find between bounding_box[0] and bounding_box[180]
        top_bound = bounding_box[0].latitude
        right_bound = bounding_box[90].longitude
        bottom_bound = bounding_box[180].latitude
        left_bound = bounding_box[270].longitude

        #print(f"\n{bounding_box}\n{top_bound},{left_bound},{bottom_bound},{right_bound}\n")

        result = self.connection.sql(f"SELECT * FROM {self.database_name} "
                                     f"WHERE Longitude BETWEEN {left_bound} AND {right_bound} "
                                     f"AND Latitude BETWEEN {bottom_bound} AND {top_bound}")

        return result.fetchall()

    @staticmethod
    def distance_between(longitude1, latitude1, longitude2, latitude2, units="km"):
        """Uses the Haversine formula in the geopy.distance library to find the difference between two coordinate points
        :param longitude1: Longitude of first point
        :param latitude1: Latitude of first point
        :param longitude2: Longitude of second point
        :param latitude2: Latitude of second point
        :param units: The unit of measurement used ('km' or 'mi')"""

        point1 = (longitude1, latitude1)
        point2 = (longitude2, latitude2)
        total_distance = 0

        if units == "mi": #miles
            total_distance = geopy.distance.distance(point1, point2).miles
        elif units == "km": #kilometers
            total_distance = geopy.distance.distance(point1, point2).km
        else: #any other unit of measurement
            pass

        return total_distance

    def location_search(self, name=None, location_type = None, city = None, address=None, state=None, zipcode=None ):
        """Given a name, address, latitude, OR longitude, it returns a list of tuples.
        The tuple list included the name, type, longitude, latitude, and address of the location.
        :param name: name of the location
        :param city: name of city
        :param address: address of the location
        :param state: state of the location
        :param zipcode: zipcode of the location"""

        modifier = ""

        if name is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"Name ILIKE '%{name.lower()}%'"

        if location_type is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"LocationType = '{location_type.lower()}'"

        if city is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"City ILIKE '%{city.lower()}%'"

        if address is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"Address ILIKE '{address.lower()}'"

        if state is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"State ILIKE '{state.lower()}'"

        if zipcode is not None:
            modifier += "WHERE " if modifier == "" else " AND "
            modifier += f"ZipCode ILIKE '{zipcode}'"

        sql_query = f"SELECT * FROM {self.database_name} {modifier}"
        print(sql_query)

        result = self.connection.sql(sql_query)

        # fetchall returns the info in a list of tuples
        return result.fetchall()

    def __start_museums_aquarium_zoo_dataframe(self):
        """an initializer for the zoo_dataframe"""
        # Download latest version
        path = f"{self.folder}museums.csv"

        # initialize dataframe from csv file
        museum = pd.read_csv(path,
                             usecols=["Museum Name", "Street Address (Administrative Location)", "Museum Type",
                                      "City (Administrative Location)", "State (Administrative Location)",
                                      "Zip Code (Administrative Location)", "Latitude", "Longitude"],
                             )

        museum = museum.rename(columns={"Museum Name": "Name",
                                        "Museum Type": "LocationType",
                                        "Street Address (Administrative Location)": "Address",
                                        "City (Administrative Location)": "City",
                                        "State (Administrative Location)": "State",
                                        "Zip Code (Administrative Location)": "ZipCode",
                                        })

        # adds a new column called countries with every entry being "USA"
        museum["Country"] = ["USA" for _ in range(len(museum))]

        # reformats the column order to allow for concatenation
        museum = museum[
            ["Name", "LocationType", "Latitude", "Longitude", "Address", "City", "State", "Country", "ZipCode"]]

        return museum


    def __us_hospital_locations_dataframe(self):
        path = f"{self.folder}us_hospital_locations.csv"

        # initialize dataframe from csv file
        hospital = pd.read_csv(path,
                               usecols=["NAME", "ADDRESS", "TYPE", "CITY", "STATE", "ZIP", "LATITUDE", "LONGITUDE"],
                               )
        hospital = hospital.rename(columns={"NAME": "Name",
                                            "ADDRESS": "Address",
                                            "TYPE": "LocationType",
                                            "CITY": "City",
                                            "STATE": "State",
                                            "ZIP": "ZipCode",
                                            "LATITUDE": "Latitude",
                                            "LONGITUDE": "Longitude", })

        # adds a new column called countries with every entry being "USA"
        hospital["Country"] = ["USA" for _ in range(len(hospital))]

        # reformats the column order to allow for concatenation
        hospital = hospital[
            ["Name", "LocationType", "Latitude", "Longitude", "Address", "City", "State", "Country", "ZipCode"]]

        return hospital


    def __fast_food_restaurant_dataframe(self):
        path = f"{self.folder}Fast_Food_Restaurants_US.csv"

        # initialize dataframe from csv file
        fast_food = pd.read_csv(path,
                                usecols=["name", "address", "city", "categories", "latitude", "longitude", "postalCode",
                                         "province"],
                                )

        fast_food = fast_food.rename(columns={"name": "Name",
                                              "address": "Address",
                                              "city": "City",
                                              "categories": "LocationType",
                                              "longitude": "Longitude",
                                              "latitude": "Latitude",
                                              "postalCode": "ZipCode",
                                              "province": "State"})

        # adds a new column called countries with every entry being "USA"
        fast_food["Country"] = ["USA" for _ in range(len(fast_food))]

        # reformats the column order to allow for concatenation
        fast_food = fast_food[
            ["Name", "LocationType", "Latitude", "Longitude", "Address", "City", "State", "Country", "ZipCode"]]

        return fast_food


def main():
    location_db = LocationDatabase()

    sonic_drive_in = location_db.location_search(name="Sonic", state="ca")
    print (f"Sonic Info: {len(sonic_drive_in)}")
    print (sonic_drive_in)


    #california_locations = location_db.location_search(state = "CA")
    #print (f"California Info: {california_locations.__sizeof__()}")

    #for i in range(10):
        #print (california_locations[i])

    """
    nearby_local = location_db.nearby_locations(longitude1=-121.83653,
                                                latitude1=39.7254,
                                                distance_range=10000000,
                                                units="mi",
                                                )

    print (nearby_local)
    """


if __name__ == "__main__":
    main()
