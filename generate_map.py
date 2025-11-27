import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import sys

def plot_glowing_coastline(place_name, save_filename):
    print(f"Fetching data for {place_name}...")
    
    # --- CORRECTED CONFIGURATION for large areas ---
    # Set the timeout to 3 minutes
    ox.settings.overpass_timeout = 180       
    # Increase the maximum query size (to reduce the 43 sub-queries warning)
    ox.settings.max_query_area_size = 1073741824 
    # -----------------------------------------------------------------

    try:
        # Fetch land boundary
        land = ox.geocode_to_gdf(place_name)
        
        # Fetch lighthouses
        tags = {'man_made': 'lighthouse'}
        lighthouses = ox.features_from_place(place_name, tags)
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Crucial: If data fetch fails, we exit gracefully and don't try to plot/save.
        return

    # Setup the figure with a dark background
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')

    # --- Plot the GLOWING BORDER for the Landmass ---
    # We plot the border multiple times with decreasing transparency for the glow effect.
    glow_color = '#fdfbd3' # Light yellow/white for the glow

    # Layer 1: Faint, thick outer glow
    land.plot(ax=ax, edgecolor=glow_color, linewidth=8, alpha=0.03, facecolor='none') 
    # Layer 2: Medium glow
    land.plot(ax=ax, edgecolor=glow_color, linewidth=5, alpha=0.08, facecolor='none')
    # Layer 3: Brighter, thinner inner glow
    land.plot(ax=ax, edgecolor=glow_color, linewidth=2, alpha=0.15, facecolor='none')
    # --------------------------------------------------

    # Plot the main Landmass (Dark silhouette) ON TOP of its glows
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights
    if not lighthouses.empty:
        # Layer 1: Outer glow
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=300, alpha=0.05)
        # Layer 2: Medium glow
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=100, alpha=0.15)
        # Layer 3: Core light (bright white)
        lighthouses.plot(ax=ax, color='#ffffff', markersize=15, alpha=0.9)

    # Clean up axes
    ax.set_axis_off()
    
    # Dynamic cropping
    minx, miny, maxx, maxy = land.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    # Save the file
    plt.savefig(save_filename, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Image saved to {save_filename}")

if __name__ == "__main__":
    # Get location from command line, default to Maine
    location = sys.argv[1] if len(sys.argv) > 1 else "Maine, USA"
    filename = "coastline_output.png"
    plot_glowing_coastline(location, filename)
