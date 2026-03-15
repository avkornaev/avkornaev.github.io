#!/usr/bin/env python3
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "_data" / "publication_sources.yml"
OVERRIDES_PATH = ROOT / "_data" / "publication_overrides.json"
PUBLICATIONS_JSON_PATH = ROOT / "_data" / "publications.json"
BIB_PATH = ROOT / "bibliography" / "publications.bib"


def read_simple_yaml(path):
    data = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def load_overrides(path):
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    return {item.get("key"): item for item in items if item.get("key")}


def fetch_json(url, accept):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "avkornaev.github.io publication sync",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url, accept):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "avkornaev.github.io publication sync",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def normalize_doi(value):
    if not value:
        return ""
    value = value.strip()
    value = value.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return value.lower()


def slugify(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    ascii_value = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    return ascii_value or "item"


def bibtex_key(item):
    author_token = item.get("first_author_family") or "kornaev"
    year = item.get("year") or "nodate"
    title_slug = slugify(item.get("title", ""))[:40]
    return "{}{}{}".format(slugify(author_token), year, title_slug)


def first_external_id(summary, wanted_type):
    external_ids = summary.get("external-ids", {}).get("external-id", [])
    for item in external_ids:
        if item.get("external-id-type") == wanted_type:
            return item.get("external-id-value")
    return ""


def first_external_url(summary):
    url_field = summary.get("url") or {}
    if url_field.get("value"):
        return url_field["value"]
    external_ids = summary.get("external-ids", {}).get("external-id", [])
    for item in external_ids:
        external_url = item.get("external-id-url") or {}
        url_value = external_url.get("value")
        if url_value:
            return url_value
    return ""


def parse_crossref_bibtex_authors(bibtex_text):
    match = re.search(r"author\s*=\s*\{(.+?)\}", bibtex_text, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    authors = []
    for raw_author in match.group(1).split(" and "):
        raw_author = raw_author.strip()
        if not raw_author:
            continue
        if "," in raw_author:
            family, given = [part.strip() for part in raw_author.split(",", 1)]
        else:
            parts = raw_author.split()
            family = parts[-1]
            given = " ".join(parts[:-1])
        authors.append({"given": given, "family": family, "full": raw_author})
    return authors


def get_first_author_family(authors):
    if not authors:
        return "kornaev"
    first = authors[0]
    return first.get("family") or first.get("full", "kornaev").split()[-1]


def convert_orcid_type(orcid_type):
    mapping = {
        "journal-article": "article",
        "conference-paper": "inproceedings",
        "book-chapter": "incollection",
        "preprint": "misc",
        "book": "book",
        "dissertation": "phdthesis",
    }
    return mapping.get(orcid_type, "misc")


def build_fallback_bibtex(item):
    fields = [
        ("title", item["title"]),
        ("author", item["author_bibtex"]),
        ("year", str(item["year"])),
    ]
    venue_field = "journal" if item["entry_type"] == "article" else "booktitle"
    if item.get("venue"):
        fields.append((venue_field, item["venue"]))
    if item.get("doi"):
        fields.append(("doi", item["doi"]))
    if item.get("url"):
        fields.append(("url", item["url"]))
    for link_field in ["paper", "code", "project", "slides", "dataset"]:
        if item.get(link_field):
            fields.append((link_field, item[link_field]))

    lines = ["@{}{{{},".format(item["entry_type"], item["bibtex_key"])]
    for key, value in fields:
        lines.append("  {} = {{{}}},".format(key, value))
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


def fetch_bibtex_for_doi(doi):
    doi_url = "https://doi.org/{}".format(urllib.parse.quote(doi, safe="/"))
    try:
        return fetch_text(doi_url, "application/x-bibtex")
    except urllib.error.URLError:
        return ""


def date_part(publication_date, key):
    field = publication_date.get(key) or {}
    return field.get("value")


def main():
    sources = read_simple_yaml(SOURCES_PATH)
    orcid = sources.get("orcid")
    if not orcid:
        raise SystemExit("Missing ORCID in _data/publication_sources.yml")

    overrides = load_overrides(OVERRIDES_PATH)
    works_url = "https://pub.orcid.org/v3.0/{}/works".format(orcid)
    works_payload = fetch_json(works_url, "application/json")

    items = []
    seen_keys = set()

    for group in works_payload.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]

        title = summary.get("title", {}).get("title", {}).get("value")
        if not title:
            continue

        publication_date = summary.get("publication-date") or {}
        year_raw = publication_date.get("year", {}).get("value")
        if not year_raw:
            continue

        doi = normalize_doi(first_external_id(summary, "doi"))
        item_key = doi or slugify("{}-{}".format(year_raw, title))
        if item_key in seen_keys:
            continue
        seen_keys.add(item_key)

        override = overrides.get(item_key, {})
        work_type = override.get("type") or summary.get("type") or "misc"
        year = int(year_raw)
        month = date_part(publication_date, "month")
        day = date_part(publication_date, "day")
        journal_title = summary.get("journal-title") or {}
        venue = journal_title.get("value") or override.get("venue", "")
        url = override.get("paper") or ("https://doi.org/{}".format(doi) if doi else first_external_url(summary))

        bibtex_text = fetch_bibtex_for_doi(doi) if doi else ""
        authors = parse_crossref_bibtex_authors(bibtex_text)
        if not authors:
            author_names = override.get("authors", [])
            authors = [{"given": "", "family": name, "full": name} for name in author_names]
        author_bibtex = " and ".join([author["full"] for author in authors]) if authors else "Alexei Kornaev"

        item = {
            "key": item_key,
            "title": title,
            "year": year,
            "month": int(month) if month and str(month).isdigit() else None,
            "day": int(day) if day and str(day).isdigit() else None,
            "type": work_type,
            "venue": venue,
            "doi": doi,
            "url": url,
            "paper": override.get("paper") or url,
            "code": override.get("code", ""),
            "project": override.get("project", ""),
            "slides": override.get("slides", ""),
            "dataset": override.get("dataset", ""),
            "note": override.get("note", ""),
            "authors": authors,
            "author_bibtex": author_bibtex,
            "first_author_family": get_first_author_family(authors),
            "entry_type": convert_orcid_type(work_type),
        }
        item["bibtex_key"] = override.get("bibtex_key") or bibtex_key(item)
        item["category"] = override.get("category") or (
            "conference" if work_type == "conference-paper" else
            "thesis" if "thesis" in work_type or "dissertation" in work_type else
            "publication"
        )

        if bibtex_text:
            bibtex_text = re.sub(
                r"^\s*@\w+\{[^,]+,",
                "@{}{{{},".format(item["entry_type"], item["bibtex_key"]),
                bibtex_text,
                count=1,
            )
            extra_fields = []
            for field_name in ["paper", "code", "project", "slides", "dataset"]:
                if item.get(field_name):
                    extra_fields.append("  {} = {{{}}},".format(field_name, item[field_name]))
            if extra_fields:
                bibtex_text = bibtex_text.rstrip()
                if bibtex_text.endswith("}"):
                    bibtex_text = bibtex_text[:-1].rstrip()
                    if not bibtex_text.endswith(","):
                        bibtex_text += ","
                    bibtex_text += "\n" + "\n".join(extra_fields) + "\n}"
        else:
            bibtex_text = build_fallback_bibtex(item)

        item["bibtex"] = bibtex_text
        items.append(item)
        time.sleep(0.1)

    items.sort(key=lambda item: (item["year"], item["month"] or 0, item["title"]), reverse=True)

    json_payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "ORCID",
        "items": [
            {
                key: value
                for key, value in item.items()
                if key != "bibtex" and key != "author_bibtex" and key != "first_author_family"
            }
            for item in items
        ],
    }
    PUBLICATIONS_JSON_PATH.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BIB_PATH.write_text("\n\n".join(item["bibtex"] for item in items) + "\n", encoding="utf-8")
    print("Synced {} works from ORCID {}".format(len(items), orcid))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Publication sync failed: {}".format(exc), file=sys.stderr)
        raise
