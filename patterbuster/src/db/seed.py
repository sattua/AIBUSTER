from tinydb import TinyDB
from datetime import datetime, timezone

db = TinyDB("db.json")
searches = db.table("searches")

searches.insert({
    "query": "seeded manually",
    "result": {
        "riskScore": 0.8,
        "findings": []
    },
    "createdAt": datetime.now(timezone.utc).isoformat()
})

print("\n=== SEARCHES ===")

for doc in searches.all():
    print({
        "id": str(doc.doc_id),
        **doc
    })

#searches.truncate()