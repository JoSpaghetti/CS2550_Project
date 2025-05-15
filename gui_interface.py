import tkinter as tk
from tkinter import ttk
import videomap as map

def gui():
    interface = tk.Tk(screenName="Map_GUI")
    interface.title("US Map Services GUI")
    interface.geometry("400x400")

    tab_control = ttk.Notebook(interface)

    # --- Distance Tab ---
    def get_location_code():
        try:
            loc_id_a = loc_code_1e.get()
            loc_id_b = loc_code_2e.get()
        except AttributeError:
            print ("Nothing Input")
        else:
            #print(loc_id_a, loc_id_b)
            map.distance_map(loc_id_a, loc_id_b)
        finally:
            interface.quit()

    distance_tab = ttk.Frame(tab_control)
    tab_control.add(distance_tab, text='Distance')

    tk.Label(distance_tab, text="Find Distance from Location Code", font=('Arial', 12, 'bold')).grid(row=0, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)
    tk.Label(distance_tab, text="Location Code 1:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    loc_code_1e = tk.Entry(distance_tab, width=30)
    loc_code_1e.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(distance_tab, text="Location Code 2:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    loc_code_2e = tk.Entry(distance_tab, width=30)
    loc_code_2e.grid(row=2, column=1, padx=10, pady=5)

    loc_code_b = tk.Button(distance_tab, text="Submit", command = get_location_code)
    loc_code_b.grid(row=3, column=0, columnspan=2, pady=10)

    # --- Nearby Services Tab ---
    def find_locations():
        try:
            latitude = float(lat_e.get())
            longitude = float(long_e.get())
            radius = int(rad_e.get())
            units = unit_value.get()

        except AttributeError:
            print ("Nothing Input")
        except ValueError:
            print ("Wrong Input")
        else:
            #print (latitude, longitude, radius, units)
            map.nearby_location_map(latitude, longitude, radius, units)
        finally:
            interface.quit()

    def use_current_coordinates():
        #insert current location here
        latitude = 0.0
        longitude = 0.0

        map.nearby_location_map(latitude, longitude, 100, "mi")

    nearby_tab = ttk.Frame(tab_control)
    tab_control.add(nearby_tab, text='Nearby Services')

    tk.Label(nearby_tab, text="Find Nearby Services", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)

    tk.Label(nearby_tab, text="Your Latitude:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    lat_e = tk.Entry(nearby_tab)
    lat_e.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Your Longitude:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    long_e = tk.Entry(nearby_tab)
    long_e.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Radius:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    rad_e = tk.Entry(nearby_tab)
    rad_e.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Unit:").grid(row=3, column=2, sticky="e", padx=5, pady=5)
    unit_value = tk.StringVar(nearby_tab)
    unit_value.set("km")
    unit_e = tk.OptionMenu(nearby_tab, unit_value, "km", "mi")
    unit_e.grid(row=3, column=3, padx=5, pady=5)

    find_b = tk.Button(nearby_tab, text="Find Nearby", command=find_locations)
    find_b.grid(row=5, column=0, columnspan=4, pady=10)

    curr_coord_b = tk.Button(nearby_tab, text="Current Coordinates", command=use_current_coordinates)
    curr_coord_b.grid(row=5, column=2, columnspan=4, pady=10)

    # --- Search Tab ---
    def search_location():
        try:
            name = name_e.get()
            address = addr_e.get()
            city = city_e.get()
            state = st_e.get()
            zipcode = zip_e.get()
        except AttributeError:
            pass
        finally:
            if name == "":
                name = None
            if address == "":
                address = None
            if city == "":
                city = None
            if state == "":
                state = None
            if zipcode == "":
                zipcode = None

            #print(name, address, city, state, zipcode)
            map.search_map(name, address, city, state, zipcode)
            interface.quit()


    search_tab = ttk.Frame(tab_control)
    tab_control.add(search_tab, text='Search')

    tk.Label(search_tab, text="Search For Locations", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

    fields = ['Name', 'Address', 'City', 'State', 'Zipcode']
    tk.Label(search_tab, text="Name:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    name_e = tk.Entry(search_tab, width=40)
    name_e.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(search_tab, text="Address:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    addr_e = tk.Entry(search_tab, width=40)
    addr_e.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(search_tab, text="City:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    city_e = tk.Entry(search_tab, width=40)
    city_e.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(search_tab, text="State:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
    st_e = tk.Entry(search_tab, width=40)
    st_e.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(search_tab, text="Zip Code:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
    zip_e = tk.Entry(search_tab, width=40)
    zip_e.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(search_tab, text="Submit", command=search_location).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

    tab_control.pack(expand=1, fill='both')
    interface.mainloop()

if __name__ == '__main__':
    gui()
