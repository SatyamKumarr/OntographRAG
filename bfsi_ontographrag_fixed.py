
import json
import re
from collections import Counter

INPUT_FILE = "C:\\Users\\SatyamKumar\\Downloads\\OntoGraphRAG-main\\OntoGraphRAG-main\\bfsi_ontographrag.json"
OUTPUT_FILE = "C:\\Users\\SatyamKumar\\Downloads\\OntoGraphRAG-main\\OntoGraphRAG-main\\bfsi_ontographrag_fixed.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    ontology = json.load(f)

classes = ontology.get("classes", [])
relationships = ontology.get("relationships", [])

# Collect class identifiers
class_ids = {c["id"] for c in classes}

# Generate globally unique relationship IDs
used_ids = set()

for index, rel in enumerate(relationships, start=1):
    relation_type = rel.get("name") or rel.get("id") or "RELATIONSHIP"
    source = rel.get("from", "")
    target = rel.get("to", "")

    # Preserve the relationship type in the name field.
    rel["name"] = relation_type

    # Generate an ID based on the relationship endpoints.
    base_id = re.sub(
        r"[^A-Za-z0-9_]+",
        "_",
        f"{relation_type}_{source}_{target}"
    )

    relationship_id = base_id
    suffix = 1

    while relationship_id in used_ids:
        suffix += 1
        relationship_id = f"{base_id}_{suffix}"

    rel["id"] = relationship_id
    used_ids.add(relationship_id)

# Validate relationship endpoints
errors = []

for rel in relationships:
    if rel.get("from") not in class_ids:
        errors.append(
            f"Unknown source class: {rel.get('from')}"
        )

    if rel.get("to") not in class_ids:
        errors.append(
            f"Unknown target class: {rel.get('to')}"
        )

# Validate duplicate class IDs
class_id_counts = Counter(c["id"] for c in classes)

for class_id, count in class_id_counts.items():
    if count > 1:
        errors.append(f"Duplicate class ID: {class_id}")

# Validate duplicate relationship IDs
rel_id_counts = Counter(r["id"] for r in relationships)

for rel_id, count in rel_id_counts.items():
    if count > 1:
        errors.append(f"Duplicate relationship ID: {rel_id}")

if errors:
    print("Ontology validation issues:")
    for error in errors:
        print("-", error)
else:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(ontology, f, indent=2, ensure_ascii=False)

    print("Ontology fixed successfully!")
    print("Classes:", len(classes))
    print("Relationships:", len(relationships))
    print("Unique relationship IDs:", len(used_ids))
    print("Output:", OUTPUT_FILE)
