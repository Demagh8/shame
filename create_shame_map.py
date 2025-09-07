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

################################### Next: Make the Pie Chart ##############################

# Data based on approx. annual support volumes (in millions USD equivalent)
countries = [
    "USA", "Germany", "UK", "Azerbaijan", "UAE",
    "Egypt", "Jordan", "Morocco", "Bahrain"
]
values = [4000, 300, 50, 1000, 1600, 300, 160, 120, 20]

# Assign colors: Western (first 3) in yellow-brown tones, Arabs/regional (others) in greens
colors = [
    "#FFD700", "#DAA520", "#8B4513",   # Western group
    "#006400", "#228B22", "#32CD32", "#66CDAA", "#90EE90", "#C1FFC1"  # Arab/regional group
]

fig, ax = plt.subplots(figsize=(10, 10))

# ✅ Donut chart with no labels
wedges, _ = ax.pie(
    values, labels=None, startangle=90, colors=colors,
    wedgeprops=dict(width=0.4)
)

# Prepare legend labels with volumes
country_labels = [f"{c} – {v}M USD" for c, v in zip(countries, values)]

# Add legend in the center hole
plt.legend(
    wedges, country_labels,
    loc="center", fontsize=11, title="Support Volume", title_fontsize=13
)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save image
output_path = "israel_supporters_piechart_groups_legend.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

