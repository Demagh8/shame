import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

# Path to the Natural Earth shapefile you downloaded from:
# https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/
shapefile = "./110m_cultural/ne_110m_admin_0_countries.shp"

# Load shapefile
world = gpd.read_file(shapefile)

# Countries to highlight
countries = [
    "United States of America", "Germany", "United Kingdom", "Italy", "Netherlands",
    "Canada", "Australia", "Azerbaijan", "Spain", "Egypt", "Jordan",
    "United Arab Emirates", "Bahrain", "Morocco", "Saudi Arabia"
]

# Define categories
red_list = [
    "United States of America", "Germany", "United Kingdom", "Azerbaijan",
    "Egypt", "Jordan", "United Arab Emirates", "Bahrain", "Morocco"
]
yellow_list = ["France", "Saudi Arabia"]
green_list = ["Italy", "Netherlands", "Canada", "Australia"]

def classify_country(name):
    if name in red_list:
        return "red"
    elif name in yellow_list:
        return "yellow"
    elif name in green_list:
        return "green"
    else:
        return "grey"

world["category"] = world["NAME"].apply(classify_country)

# Gall-Peters projection (Equal Area)
proj = ccrs.EqualEarth()
fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': proj})

# Plot all countries by category
color_map = {
    "red": "red",
    "yellow": "gold",
    "green": "green",
    "grey": "lightgrey"
}
for cat, color in color_map.items():
    world[world["category"] == cat].plot(
        ax=ax, transform=ccrs.PlateCarree(),
        color=color, edgecolor="black", linewidth=0.5, label=cat
    )

# Add borders/coastlines
ax.coastlines(linewidth=0.5)

# Remove margins around map
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Legend with descriptive labels
labels_map = {
    "red": "Active suppliers",
    "yellow": "Suspected / unofficial",
    "green": "Stopped suppliers",
    "grey": "Others"
}
# Create patches manually for legend
patches = [mpatches.Patch(color=color, label=label) for color, label in labels_map.items()]
ax.legend(handles=patches, loc="lower left", fontsize=16, title="Legend", title_fontsize=24)

# Save PNG
plt.savefig("countries_supplying_israel_sep2025.png", dpi=300, bbox_inches="tight")
plt.show()
