import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd
import sys

def plot_glowing_coastline(place_name, save_filename):
    print(f"Fetching data for {place_name}...")
    
    # --- GLOBAL CONFIGURATION (Timeout only) ---
    ox.settings.overpass_timeout = 180       
    # We rely on the internal logic to set max_query_area_size unless explicitly overridden below
    # -----------------------------------------------------------------------------

    # Define Bounding Boxes
    # Bbox for the entire state of Maine (used for detailed land fetch)
    maine_bbox = (47.5, 42.9, -66.9, -71.2) 
    # Bbox for fetching lighthouses in the central/southern Maine coast
    lighthouse_bbox = (44.20, 43.48, -69.00, -70.25) 
    bbox_tuple = lighthouse_bbox 

    try:
        # --- NEW LOGIC: Conditional Land Fetch (Detailed Coastline) ---
        
        # Check if the user is running the entire state map ("Maine, USA")
        if "maine" in place_name.lower() and len(place_name.split(',')) < 3:
            # Override max_query_area_size ONLY for this slow, complex query
            ox.settings.max_query_area_size = 1073741824 
            
            # Fetch the detailed geographic coastline (slow but detailed)
            tags_coastline = {'natural': 'coastline'}
            land = ox.features_from_bbox(maine_bbox, tags_coastline)
            print("Using detailed coastline query...")
        else:
            # For small/specific areas (Boothbay), use the fast administrative boundary fetch
            land = ox.geocode_to_gdf(place_name)
            print("Using administrative boundary query (fast)...")
        # -----------------------------------------------------------------------------
        
        # Fetch Lighthouses using the BBox
        tags_lights = {'man_made': 'lighthouse'}
        lighthouses = ox.features_from_bbox(bbox_tuple, tags_lights)
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Setup the figure with a dark background
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')

    # --- Plot the GLOWING BORDER (Increased Brightness) ---
    glow_color = '#fdfbd3' 

    # Layer 1: Very thick, outer glow (More prominent)
    land.plot(ax=ax, edgecolor=glow_color, linewidth=12, alpha=0.07, facecolor='none') 
    # Layer 2: Medium glow (Thicker and brighter than before)
    land.plot(ax=ax, edgecolor=glow_color, linewidth=8, alpha=0.15, facecolor='none')
    # Layer 3: Brighter, thinner inner glow
    land.plot(ax=ax, edgecolor=glow_color, linewidth=3, alpha=0.3, facecolor='none')
    # ------------------------------------------------------

    # Plot the main Landmass (Dark silhouette) ON TOP of its glows
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights
    if not lighthouses.empty:
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=300, alpha=0.05)
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=100, alpha=0.15)
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
    location = sys.argv[1] if len(sys.argv) > 1 else "Maine, USA"
    filename = "coastline_output.png"
    plot_glowing_coastline(location, filename)
