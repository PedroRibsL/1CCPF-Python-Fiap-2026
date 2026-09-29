from idlelib import query
from pathlib import Path
import json, csv

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "leads.json"

# CRUD
# CREATE
# READ
# UPDATE
# DELETE

# READ
def read_leads():
    if not DB_PATH.exists():
        return []

    try:
        return json.loads(DB_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def save_leads(leads):
    DB_PATH.write_text(
        json.dumps(leads, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

# CREATE
def create_lead(lead_dict):
    leads = read_leads() # lista de dicionarios de leads
    leads.append(lead_dict)
    save_leads(leads)
    return lead_dict

# EXPORT LEADS COMO CSV
def export_csv():
    """Exporta os leads para CSV e RETORNA o caminho do aquivo criado"""
    path_csv = DATA_DIR / "leads.csv"

    leads = read_leads() # LISTA - ARRAY!

    try:
        with path_csv.open("w", newline="", encoding="utf-8") as file_csv:
           writer = csv.DictWriter(file_csv, fieldnames=leads[0].keys())
           writer.writeheader()
           for row in leads:
               writer.writerow(row)
        return path_csv
    except FileNotFoundError:
        return None

# READ LEADS FORM QUERY/SEARCH
def read_leads_search(query):
    leads = read_leads()
    results = []

    for i, lead in enumerate(leads):
        txt_lead = f"{lead["name"]} {lead["email"]} {lead["company"]}".lower()
        # print(txt_Lead)

        if query.lower() in txt_lead:
            results.append((i, lead)) # (0, {"name": "Alexandre" ...})

    return results

#UPDATE
def update_lead(index, new_data):
    leads = read_leads()
    if index < 0 or index >= len(leads):
        return None
    leads[index].update(new_data)
    save_leads(leads)
    return leads[index]

#DELETE
def delete_lead(index):
    leads = read_leads()
    if index < 0 or index >= len(leads):
        return None
    removed = leads.pop(index)
    save_leads(leads)
    return removed

