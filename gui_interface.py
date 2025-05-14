import tkinter as tk
from tkinter import ttk, messagebox
import math
import pandas as pd

# Load data
hospitals_df = pd.read_csv("database/us_hospital_locations.csv")
restaurants_df = pd.read_csv("database/Fast_Food_Restaurants_US.csv")
museums_df = pd.read_csv("database/museums.csv")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def find_distances_from_location_code(code):
    try:
        base = hospitals_df[hospitals_df['Provider ID'] == int(code)].iloc[0]
        base_lat, base_lon = base['LATITUDE'], base['LONGITUDE']
        distances = []
        for _, row in hospitals_df.iterrows():
            dist = haversine(base_lat, base_lon, row['LATITUDE'], row['LONGITUDE'])
            distances.append((row['NAME'], row['ADDRESS'], row['CITY'], row['STATE'], f"{dist:.2f} km"))
        return sorted(distances, key=lambda x: float(x[-1].split()[0]))[:10]
    except Exception as e:
        return [("Error", str(e), "", "", "")]

def find_nearby(df, lat, lon, radius, unit="km"):
    R = 6371 if unit == "km" else 3958.8  # km or miles
    nearby = []
    for _, row in df.iterrows():
        dist_km = haversine(lat, lon, row['LATITUDE'], row['LONGITUDE'])
        dist = dist_km if unit == "km" else dist_km * 0.621371
        if dist <= radius:
            nearby.append((row['NAME'], dist))
    return sorted(nearby, key=lambda x: x[1])

def gui():
    interface = tk.Tk(screenName="Map_GUI")
    interface.title("US Map Services GUI")
    interface.geometry("750x600")

    tab_control = ttk.Notebook(interface)

    # --- Distance Tab ---
    distance_tab = ttk.Frame(tab_control)
    tab_control.add(distance_tab, text='Distance')

    tk.Label(distance_tab, text="Location Code:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    code_entry = tk.Entry(distance_tab, width=30)
    code_entry.grid(row=0, column=1, padx=10, pady=10)

    result_listbox = tk.Text(distance_tab, height=15, width=70)
    result_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def display_distances():
        code = code_entry.get()
        results = find_distances_from_location_code(code)
        result_listbox.delete("1.0", tk.END)
        for name, addr, city, state, dist in results:
            result_listbox.insert(tk.END, f"{name}, {addr}, {city}, {state} - {dist}\n")

    tk.Button(distance_tab, text="Submit", command=display_distances).grid(row=1, column=0, columnspan=2)

    # --- Nearby Services Tab ---
    nearby_tab = ttk.Frame(tab_control)
    tab_control.add(nearby_tab, text='Nearby Services')

    tk.Label(nearby_tab, text="Your Latitude:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    user_lat = tk.Entry(nearby_tab)
    user_lat.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Your Longitude:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    user_lon = tk.Entry(nearby_tab)
    user_lon.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Radius:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    radius = tk.Entry(nearby_tab)
    radius.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Unit:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
    unit_var = tk.StringVar(value="km")
    tk.OptionMenu(nearby_tab, unit_var, "km", "miles").grid(row=2, column=3, padx=5, pady=5)

    tk.Label(nearby_tab, text="Category:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    category_var = tk.StringVar(value="Hospitals")
    tk.OptionMenu(nearby_tab, category_var, "All", "Hospitals", "Restaurants", "Museums").grid(row=3, column=1, padx=5, pady=5)

    nearby_result_box = tk.Text(nearby_tab, height=12, width=70)
    nearby_result_box.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def show_nearby():
        try:
            lat = float(user_lat.get())
            lon = float(user_lon.get())
            r = float(radius.get())
            unit = unit_var.get()
            cat = category_var.get()

            results = []

            if cat == "Hospitals" or cat == "All":
                results += find_nearby(hospitals_df, lat, lon, r, unit)
            if cat == "Restaurants" or cat == "All":
                results += find_nearby(restaurants_df, lat, lon, r, unit)
            if cat == "Museums" or cat == "All":
                results += find_nearby(museums_df, lat, lon, r, unit)

            results = sorted(results, key=lambda x: x[1])

            nearby_result_box.delete(1.0, tk.END)
            if results:
                for name, dist in results:
                    nearby_result_box.insert(tk.END, f"{name} - {dist:.2f} {unit}\n")
            else:
                nearby_result_box.insert(tk.END, "No nearby results found.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    tk.Button(nearby_tab, text="Find Nearby", command=show_nearby).grid(row=4, column=0, columnspan=4, pady=10)

    # --- Search Tab ---
    search_tab = ttk.Frame(tab_control)
    tab_control.add(search_tab, text='Search')

    fields = ['Name', 'Address', 'City', 'State', 'Zipcode']
    entries = {}

    for i, label in enumerate(fields):
        tk.Label(search_tab, text=label + ":").grid(row=i, column=0, sticky="e", padx=10, pady=5)
        entry = tk.Entry(search_tab, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label.lower()] = entry

    def submit_search():
        name = entries['name'].get().lower()
        address = entries['address'].get().lower()
        city = entries['city'].get().lower()
        state = entries['state'].get().lower()
        zipcode = entries['zipcode'].get()

        results = []

        for _, row in hospitals_df.iterrows():
            if (name in str(row['NAME']).lower() and
                address in str(row['ADDRESS']).lower() and
                city in str(row['CITY']).lower() and
                state in str(row['STATE']).lower() and
                zipcode in str(row.get('ZIP', '')).lower()):
                results.append(f"{row['NAME']} - {row['ADDRESS']}, {row['CITY']}, {row['STATE']} {row.get('ZIP', '')}")

        search_result_box.delete(1.0, tk.END)
        if results:
            for line in results:
                search_result_box.insert(tk.END, line + "\n")
        else:
            search_result_box.insert(tk.END, "No matches found.")

    tk.Button(search_tab, text="Submit", command=submit_search).grid(row=len(fields), column=0, columnspan=2, pady=10)

    search_result_box = tk.Text(search_tab, height=10, width=70)
    search_result_box.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=10)

    tab_control.pack(expand=1, fill='both')
    interface.mainloop()

if __name__ == '__main__':
    gui()
