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
3. .github/workflows/generate.yml
This is the "magic" file. It tells GitHub: "When I click a button, start a computer, install Python, generate the map, and save the image for me."

YAML

name: Generate Coastline Map

on:
  workflow_dispatch:
    inputs:
      location:
        description: 'Location to map (e.g., Maine, USA)'
        required: true
        default: 'Maine, USA'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run script
      run: python generate_map.py "${{ inputs.location }}"

    - name: Upload Image Artifact
      uses: actions/upload-artifact@v4
      with:
        name: coastline-map
        path: coastline_output.png
