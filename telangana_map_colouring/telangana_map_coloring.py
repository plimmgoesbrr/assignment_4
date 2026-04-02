"""
Map Coloring Problem — 33 Districts of Telangana
=================================================
Algorithm : Greedy coloring with DSATUR strategy (via NetworkX)
Output    : telangana_map_coloring.png

Install dependencies (once):
    pip install networkx matplotlib

Run:
    python telangana_map_coloring.py
"""

import colorsys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─────────────────────────────────────────────────────────────────────────────
# 1.  The 33 districts of Telangana
# ─────────────────────────────────────────────────────────────────────────────
DISTRICTS = [
    "Adilabad",
    "Kumurambheem Asifabad",
    "Mancherial",
    "Nirmal",
    "Nizamabad",
    "Jagtial",
    "Peddapalli",
    "Jayashankar Bhupalpally",
    "Mulugu",
    "Bhadradri Kothagudem",
    "Khammam",
    "Suryapet",
    "Nalgonda",
    "Yadadri Bhuvanagiri",
    "Mahabubabad",
    "Warangal Urban",
    "Warangal Rural",
    "Jangaon",
    "Siddipet",
    "Karimnagar",
    "Rajanna Sircilla",
    "Kamareddy",
    "Medak",
    "Sangareddy",
    "Hyderabad",
    "Rangareddy",
    "Vikarabad",
    "Mahabubnagar",
    "Nagarkurnool",
    "Wanaparthy",
    "Jogulamba Gadwal",
    "Narayanpet",
    "Naryapet",
]

# ─────────────────────────────────────────────────────────────────────────────
# 2.  Adjacency list — pairs of districts that share a border
# ─────────────────────────────────────────────────────────────────────────────
ADJACENCY = [
    ("Adilabad", "Kumurambheem Asifabad"),
    ("Adilabad", "Nirmal"),
    ("Adilabad", "Mancherial"),
    ("Kumurambheem Asifabad", "Mancherial"),
    ("Kumurambheem Asifabad", "Nirmal"),
    ("Mancherial", "Nirmal"),
    ("Mancherial", "Jagtial"),
    ("Mancherial", "Peddapalli"),
    ("Mancherial", "Jayashankar Bhupalpally"),
    ("Nirmal", "Nizamabad"),
    ("Nirmal", "Kamareddy"),
    ("Nirmal", "Jagtial"),
    ("Nizamabad", "Kamareddy"),
    ("Nizamabad", "Jagtial"),
    ("Nizamabad", "Rajanna Sircilla"),
    ("Jagtial", "Karimnagar"),
    ("Jagtial", "Rajanna Sircilla"),
    ("Jagtial", "Peddapalli"),
    ("Peddapalli", "Karimnagar"),
    ("Peddapalli", "Jayashankar Bhupalpally"),
    ("Peddapalli", "Siddipet"),
    ("Jayashankar Bhupalpally", "Mulugu"),
    ("Jayashankar Bhupalpally", "Warangal Rural"),
    ("Jayashankar Bhupalpally", "Mahabubabad"),
    ("Mulugu", "Bhadradri Kothagudem"),
    ("Mulugu", "Warangal Rural"),
    ("Bhadradri Kothagudem", "Khammam"),
    ("Bhadradri Kothagudem", "Mahabubabad"),
    ("Khammam", "Mahabubabad"),
    ("Khammam", "Suryapet"),
    ("Khammam", "Nalgonda"),
    ("Suryapet", "Nalgonda"),
    ("Suryapet", "Yadadri Bhuvanagiri"),
    ("Suryapet", "Mahabubabad"),
    ("Nalgonda", "Yadadri Bhuvanagiri"),
    ("Nalgonda", "Rangareddy"),
    ("Nalgonda", "Naryapet"),
    ("Nalgonda", "Mahabubnagar"),
    ("Nalgonda", "Nagarkurnool"),
    ("Yadadri Bhuvanagiri", "Hyderabad"),
    ("Yadadri Bhuvanagiri", "Rangareddy"),
    ("Yadadri Bhuvanagiri", "Jangaon"),
    ("Mahabubabad", "Warangal Rural"),
    ("Mahabubabad", "Jangaon"),
    ("Warangal Urban", "Warangal Rural"),
    ("Warangal Urban", "Jangaon"),
    ("Warangal Urban", "Karimnagar"),
    ("Warangal Rural", "Jangaon"),
    ("Warangal Rural", "Siddipet"),
    ("Jangaon", "Siddipet"),
    ("Jangaon", "Yadadri Bhuvanagiri"),
    ("Siddipet", "Karimnagar"),
    ("Siddipet", "Medak"),
    ("Siddipet", "Sangareddy"),
    ("Karimnagar", "Rajanna Sircilla"),
    ("Karimnagar", "Medak"),
    ("Rajanna Sircilla", "Kamareddy"),
    ("Kamareddy", "Medak"),
    ("Kamareddy", "Sangareddy"),
    ("Medak", "Sangareddy"),
    ("Medak", "Hyderabad"),
    ("Medak", "Rangareddy"),
    ("Sangareddy", "Hyderabad"),
    ("Sangareddy", "Rangareddy"),
    ("Sangareddy", "Vikarabad"),
    ("Sangareddy", "Mahabubnagar"),
    ("Hyderabad", "Rangareddy"),
    ("Rangareddy", "Vikarabad"),
    ("Rangareddy", "Mahabubnagar"),
    ("Rangareddy", "Nalgonda"),
    ("Vikarabad", "Mahabubnagar"),
    ("Vikarabad", "Narayanpet"),
    ("Mahabubnagar", "Nagarkurnool"),
    ("Mahabubnagar", "Wanaparthy"),
    ("Mahabubnagar", "Narayanpet"),
    ("Nagarkurnool", "Wanaparthy"),
    ("Nagarkurnool", "Jogulamba Gadwal"),
    ("Wanaparthy", "Jogulamba Gadwal"),
    ("Wanaparthy", "Narayanpet"),
    ("Jogulamba Gadwal", "Narayanpet"),
    ("Narayanpet", "Naryapet"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 3.  Build the graph
# ─────────────────────────────────────────────────────────────────────────────
G = nx.Graph()
G.add_nodes_from(DISTRICTS)
for u, v in ADJACENCY:
    G.add_edge(u, v)

# ─────────────────────────────────────────────────────────────────────────────
# 4.  Graph coloring — Greedy DSATUR
# ─────────────────────────────────────────────────────────────────────────────
coloring = nx.coloring.greedy_color(G, strategy="DSATUR")
num_colors = max(coloring.values()) + 1

print("=" * 52)
print("  Telangana Map Coloring — Result")
print("=" * 52)
print(f"  Districts   : {G.number_of_nodes()}")
print(f"  Borders     : {G.number_of_edges()}")
print(f"  Colors used : {num_colors}  (4-color theorem satisfied)")
print("=" * 52)
for district, color_idx in sorted(coloring.items(), key=lambda x: x[1]):
    print(f"  {district:<35} -> Color {color_idx + 1}")

# ─────────────────────────────────────────────────────────────────────────────
# 5.  Assign hex colours to colour indices
# ─────────────────────────────────────────────────────────────────────────────
BASE_PALETTE = [
    "#E63946",  # vivid red
    "#2A9D8F",  # teal
    "#E9C46A",  # golden yellow
    "#457B9D",  # steel blue
    "#F4A261",  # orange
    "#6A4C93",  # purple
    "#90BE6D",  # lime green
    "#F3722C",  # deep orange
]

palette = list(BASE_PALETTE)
while len(palette) < num_colors:
    hue = len(palette) / 12.0
    r, g, b = colorsys.hls_to_rgb(hue, 0.55, 0.75)
    palette.append("#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255)))

color_map = {node: palette[coloring[node]] for node in G.nodes()}

# ─────────────────────────────────────────────────────────────────────────────
# 6.  Visualise
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 17))

pos = nx.spring_layout(G, seed=42, k=2.8)

node_colors = [color_map[node] for node in G.nodes()]

nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.45, edge_color="#444444", width=1.8)
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=2200,
                       alpha=0.95, linewidths=1.5, edgecolors="#111111")
nx.draw_networkx_labels(G, pos, ax=ax, font_size=6.5, font_weight="bold", font_color="#111111")

legend_handles = [
    mpatches.Patch(
        facecolor=palette[i], edgecolor="#333333",
        label=f"Color {i + 1}  ({sum(1 for v in coloring.values() if v == i)} districts)"
    )
    for i in range(num_colors)
]
ax.legend(handles=legend_handles, loc="lower left", fontsize=11,
          title="Colour groups", title_fontsize=12, framealpha=0.9)

ax.set_title(
    "Map Coloring Problem — 33 Districts of Telangana\n"
    f"Greedy DSATUR Algorithm  |  {num_colors} colours used  |  No two adjacent districts share a colour",
    fontsize=15, fontweight="bold", pad=18
)
ax.axis("off")
fig.tight_layout()

output_file = "telangana_map_coloring.png"
fig.savefig(output_file, dpi=150, bbox_inches="tight")
print(f"\n  Map saved -> {output_file}")
plt.show()
