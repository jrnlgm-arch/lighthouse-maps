import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import sys

def plot_glowing_coastline(place_name, save_filename):
    print(f"Fetching data for {place_name}...")
    
    # Configure OSMnx for larger queries if needed (optional, but good for states)
    ox.settings.overpass_settings = '[out:json][timeout:180][maxsize:1073741824];' 

    try:
        land = ox.geocode_to_gdf(place_name)
        tags = {'man_made': 'lighthouse'}
        lighthouses = ox.features_from_place(place_name, tags)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')

    # --- NEW: Plot the GLOWING BORDER for the Landmass ---
    # We plot the land border multiple times with decreasing transparency
    # and slightly offset linewidths to create the glow effect.
    # The color here should be the glow color (e.g., light yellow/white)
    
    # Layer 1: Faint, thick outer glow for the entire landmass
    land.plot(ax=ax, edgecolor='#fdfbd3', linewidth=8, alpha=0.03, facecolor='none') 
    # Layer 2: Medium glow
    land.plot(ax=ax, edgecolor='#fdfbd3', linewidth=5, alpha=0.08, facecolor='none')
    # Layer 3: Brighter, thinner inner glow
    land.plot(ax=ax, edgecolor='#fdfbd3', linewidth=2, alpha=0.15, facecolor='none')
    # --- END NEW GLOW ---

    # Plot the main Landmass (Dark silhouette) ON TOP of its glows
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights (Existing logic, ensure it's after the land fill)
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
    location = sys.argv[1] if len(sys.argv) > 1 else "Maine, USA"
    filename = "coastline_output.png"
    plot_glowing_coastline(location, filename)
