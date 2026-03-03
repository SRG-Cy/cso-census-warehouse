import json

with open("data/fy001_population.json") as f:
    data = json.load(f)

# See the top level keys
print("Top level keys:", list(data.keys()))

# See the dataset label
print("Label:", data.get("label"))

# See the dimensions (what categories exist)
dims = data.get("id", [])
print("\nDimensions:", dims)

for dim in dims:
    dim_data = data["dimension"][dim]
    print(f"\n--- {dim} ---")
    categories = dim_data["category"]["label"]
    for k, v in list(categories.items())[:10]:
        print(f"  {k}: {v}")