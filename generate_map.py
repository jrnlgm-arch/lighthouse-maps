import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import sys

def plot_glowing_coastline(place_name, save_filename):
    print(f"Fetching data for {place_name}...")
    
    # --- CORRECTED CONFIGURATION for large areas ---
    ox.settings.overpass_timeout = 180       
    ox.settings.max_query_area_size = 1073741824 
    # -----------------------------------------------------------------

    # Final Bounding Box for the desired Maine Coastline area (Lat/Lon)
    # (North, South, East, West)
    north = 44.20
    south = 43.48
    east = -69.00
    west = -70.25
    
    # --- NEW: Create the required bounding box tuple ---
    bbox_tuple = (north, south, east, west)
    # ---------------------------------------------------

    try:
        # 1. Fetch Land (Coastline) - Use the place_name argument for the general land shape
        land = ox.geocode_to_gdf(place_name)
        
        # 2. Fetch Lighthouses using the BBox to guarantee inclusion
        tags_lights = {'man_made': 'lighthouse'}
        
        # --- CORRECTED FUNCTION CALL ---
        # Passing the bbox as a single tuple instead of four separate arguments
        lighthouses = ox.features_from_bbox(bbox_tuple, tags_lights) 
        # -------------------------------
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 1. Setup the figure and axis
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black') 
    ax.set_facecolor('black')

    # Plot the GLOWING BORDER for the Landmass
    glow_color = '#fdfbd3' 
    land.plot(ax=ax, edgecolor=glow_color, linewidth=8, alpha=0.03, facecolor='none') 
    land.plot(ax=ax, edgecolor=glow_color, linewidth=5, alpha=0.08, facecolor='none')
    land.plot(ax=ax, edgecolor=glow_color, linewidth=2, alpha=0.15, facecolor='none')

    # Plot the main Landmass (Dark silhouette)
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights (Markers only)
    if not lighthouses.empty:
        # Plot the glow layers and core light
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=300, alpha=0.05)
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=100, alpha=0.15)
        lighthouses.plot(ax=ax, color='#ffffff', markersize=15, alpha=0.9, zorder=3)
        
    # Final map styling
    ax.set_axis_off()
    
    # Dynamic cropping
    minx, miny, maxx, maxy = land.total_bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    # Save the figure
    plt.savefig(save_filename, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Image saved to {save_filename}")

if __name__ == "__main__":
    location = sys.argv[1] if len(sys.argv) > 1 else "Maine, USA"
    filename = "coastline_output.png"
    plot_glowing_coastline(location, filename)
