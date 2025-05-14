import tkinter as tk
from tkinter import ttk

def gui():
    interface = tk.Tk(screenName="Map_GUI")
    interface.title("US Map Services GUI")
    interface.geometry("800x650")

    tab_control = ttk.Notebook(interface)

    # --- Distance Tab ---
    distance_tab = ttk.Frame(tab_control)
    tab_control.add(distance_tab, text='Distance')

    tk.Label(distance_tab, text="Find Distance from Location Code", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(distance_tab, text="Location Code:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    tk.Entry(distance_tab, width=30).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(distance_tab, text="Submit").grid(row=2, column=0, columnspan=2, pady=10)
    tk.Text(distance_tab, height=15, width=70).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # --- Nearby Services Tab ---
    nearby_tab = ttk.Frame(tab_control)
    tab_control.add(nearby_tab, text='Nearby Services')

    tk.Label(nearby_tab, text="Find Nearby Services", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)

    tk.Label(nearby_tab, text="Your Latitude:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(nearby_tab).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Your Longitude:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(nearby_tab).grid(row=2, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Radius:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(nearby_tab).grid(row=3, column=1, padx=5, pady=5)

    tk.Label(nearby_tab, text="Unit:").grid(row=3, column=2, sticky="e", padx=5, pady=5)
    tk.OptionMenu(nearby_tab, tk.StringVar(value="km"), "km", "miles").grid(row=3, column=3, padx=5, pady=5)

    tk.Label(nearby_tab, text="Category:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    tk.OptionMenu(nearby_tab, tk.StringVar(value="All"), "All", "Hospitals", "Restaurants", "Museums").grid(row=4, column=1, padx=5, pady=5)

    tk.Button(nearby_tab, text="Find Nearby").grid(row=5, column=0, columnspan=4, pady=10)
    tk.Text(nearby_tab, height=12, width=70).grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    # --- Search Tab ---
    search_tab = ttk.Frame(tab_control)
    tab_control.add(search_tab, text='Search')

    tk.Label(search_tab, text="Search Hospital Records", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

    fields = ['Name', 'Address', 'City', 'State', 'Zipcode']
    for i, field in enumerate(fields):
        tk.Label(search_tab, text=field + ":").grid(row=i+1, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(search_tab, width=40).grid(row=i+1, column=1, padx=10, pady=5)

    tk.Button(search_tab, text="Submit").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
    tk.Text(search_tab, height=10, width=70).grid(row=len(fields)+2, column=0, columnspan=2, padx=10, pady=10)

    tab_control.pack(expand=1, fill='both')
    interface.mainloop()

if __name__ == '__main__':
    gui()
