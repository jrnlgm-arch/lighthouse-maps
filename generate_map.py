import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import sys

def plot_glowing_coastline(place_name, save_filename):
    print(f"Fetching data for {place_name}...")
    
    try:
        land = ox.geocode_to_gdf(place_name)
        tags = {'man_made': 'lighthouse'}
        lighthouses = ox.features_from_place(place_name, tags)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')

    # Plot Land
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights
    if not lighthouses.empty:
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=300, alpha=0.05)
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=100, alpha=0.15)
        lighthouses.plot(ax=ax, color='#ffffff', markersize=15, alpha=0.9)

    ax.set_axis_off()
    
    # Dynamic cropping
    minx, miny, maxx, maxy = land.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.savefig(save_filename, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Image saved to {save_filename}")

if __name__ == "__main__":
    # Default to Maine if no argument provided
    location = sys.argv[1] if len(sys.argv) > 1 else "Maine, USA"
    filename = "coastline_output.png"
    plot_glowing_coastline(location, filename)
