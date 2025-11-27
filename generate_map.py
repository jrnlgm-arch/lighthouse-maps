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
    # The user-provided coordinates: (North, South, East, West)
    north = 44.20
    south = 43.48
    east = -69.00
    west = -70.25
    
    try:
        # 1. Fetch Land (Coastline) - Use the place_name argument for the general land shape
        land = ox.geocode_to_gdf(place_name)
        
        # 2. Fetch Lighthouses using the BBox to guarantee inclusion
        tags_lights = {'man_made': 'lighthouse'}
        lighthouses = ox.features_from_bbox(north, south, east, west, tags_lights)
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 1. Setup the figure and axis
    # INCREASED FIGURE WIDTH to make room for the external key
    fig, ax = plt.subplots(figsize=(15, 12), facecolor='black') 
    ax.set_facecolor('black')

    # 2. Adjust subplot to create space on the right for the key (shrinks map width to 75%)
    fig.subplots_adjust(right=0.75) 

    # Plot the GLOWING BORDER for the Landmass
    glow_color = '#fdfbd3' 
    land.plot(ax=ax, edgecolor=glow_color, linewidth=8, alpha=0.03, facecolor='none') 
    land.plot(ax=ax, edgecolor=glow_color, linewidth=5, alpha=0.08, facecolor='none')
    land.plot(ax=ax, edgecolor=glow_color, linewidth=2, alpha=0.15, facecolor='none')

    # Plot the main Landmass (Dark silhouette)
    land.plot(ax=ax, color='#0a0a0a', edgecolor='#222222', linewidth=0.5)

    # Plot Lights AND External Key
    if not lighthouses.empty:
        # Plot the light markers
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=300, alpha=0.05)
        lighthouses.plot(ax=ax, color='#fdfbd3', markersize=100, alpha=0.15)
        lighthouses.plot(ax=ax, color='#ffffff', markersize=15, alpha=0.9, zorder=3)

        
        # --- Draw the External Key and Connector Lines ---
        
        # Determine the key position (normalized figure coordinates, 0 to 1)
        key_start_x = 0.77  # Start text at 77% across the figure width
        key_start_y = 0.95  # Start near the top
        y_step = 0.03       # Space between each name

        # Filter out lighthouses without names
        named_lighthouses = lighthouses[lighthouses['name'].notna()]
        
        # Loop through each named lighthouse
        for i, (index, row) in enumerate(named_lighthouses.iterrows()):
            x_data = row.geometry.x
            y_data = row.geometry.y
            label = row['name']
            
            # Calculate the target position for the text label (in figure coordinates)
            text_y_fig = key_start_y - i * y_step
            text_x_fig = key_start_x
            
            # 1. Draw the connecting line from the light to the key area
            x_map, y_map = ax.transData.transform((x_data, y_data))
            inv = fig.transFigure.inverted().transform
            x_fig_start, y_fig_start = inv((x_map, y_map))

            line = plt.Line2D(
                [x_fig_start, text_x_fig - 0.005], # X coordinates
                [y_fig_start, text_y_fig],         # Y coordinates
                transform=fig.transFigure,         # Plot relative to the entire figure
                color='white',
                linewidth=0.5,
                alpha=0.4
            )
            fig.add_artist(line)

            # 2. Add the text label
            fig.text(
                text_x_fig, 
                text_y_fig, 
                label,
                transform=fig.transFigure,
                color='white',
                fontsize=8,
                ha='left',
                va='center'
            )

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
