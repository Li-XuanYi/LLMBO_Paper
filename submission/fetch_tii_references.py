"""Fetch publisher-deposited Crossref metadata for the TII replacement references."""

import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
records = []
entries = []
for doi in (ROOT / "tii_replacement_dois.txt").read_text().splitlines():
    request = Request("https://api.crossref.org/works/" + quote(doi, safe=""),
                      headers={"User-Agent": "CitationVerification/1.0"})
    with urlopen(request, timeout=30) as response:
        message = json.load(response)["message"]
    records.append(message)
    year = next(message[field]["date-parts"][0][0]
                for field in ("published-print", "published", "issued", "created")
                if field in message)
    author = " and ".join(a.get("family", "") + ", " + a.get("given", "")
                          for a in message.get("author", []))
    fields = {
        "author": author,
        "title": message["title"][0],
        "journal": message["container-title"][0],
        "year": str(year),
        "volume": message.get("volume", ""),
        "number": message.get("issue", ""),
        "pages": message.get("page", "").replace("-", "--"),
        "doi": message["DOI"],
        "url": "https://doi.org/" + message["DOI"],
    }
    key = "TII" + doi.rsplit(".", 1)[1]
    entry = "@article{" + key + ",\n" + "\n".join(
        "  " + name + " = {" + value + "}," for name, value in fields.items() if value
    ) + "\n}"
    entries.append(entry)
    print(json.dumps(fields, ensure_ascii=True), flush=True)
(ROOT / "tii_replacement_crossref.json").write_text(
    json.dumps(records, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
(ROOT / "tii_replacement_verified.bib").write_text(
    "\n\n".join(entries) + "\n", encoding="utf-8")
