"""Read the site's literal BibTeX and derive its public JSON/Markdown views.

Standard library only. Supports braced/quoted values, nested braces and month
tokens; rejects BibTeX macros and concatenation instead of silently losing data.
"""

import json
import re
import unicodedata


def parse_bibtex(text):
    entries = []
    pos = 0
    while pos < len(text):
        whitespace = re.match(r"(?:\s|%[^\n]*(?:\n|$))*", text[pos:])
        pos += whitespace.end()
        if pos == len(text):
            break
        header = re.match(r"@(\w+)\s*\{\s*([^,]+),", text[pos:])
        if not header:
            raise ValueError("Expected a BibTeX entry near {!r}".format(text[pos:pos + 60]))
        entry = {"entry_type": header[1].lower(), "bibtex_key": header[2].strip()}
        pos += header.end()
        while True:
            pos += re.match(r"[\s,]*", text[pos:]).end()
            if pos >= len(text):
                raise ValueError("Unclosed entry " + entry["bibtex_key"])
            if text[pos] == "}":
                pos += 1
                break
            field = re.match(r"([\w-]+)\s*=\s*", text[pos:])
            if not field:
                raise ValueError("Unsupported field near {!r}".format(text[pos:pos + 60]))
            name = field[1].lower()
            pos += field.end()
            start = pos
            if text[pos] in '{"':
                delimiter = text[pos]
                pos += 1
                start = pos
                depth = 1 if delimiter == "{" else 0
                while pos < len(text):
                    char = text[pos]
                    if char == "\\":
                        pos += 2
                        continue
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                        if delimiter == "{" and depth == 0:
                            break
                    elif char == '"' and delimiter == '"' and depth == 0:
                        break
                    pos += 1
                if pos >= len(text):
                    raise ValueError("Unclosed field " + name)
                value = text[start:pos]
                pos += 1
            else:
                token = re.match(r"[\w.-]+", text[pos:])
                months = "jan feb mar apr may jun jul aug sep sept oct nov dec january february march april june july august september october november december".split()
                if not token or not (token[0].isdigit() or token[0].lower() in months):
                    raise ValueError("Expand BibTeX macros into literal values near " + text[pos:pos + 60])
                value = token[0]
                pos += token.end()
            if name in entry:
                raise ValueError("Duplicate field " + name)
            entry[name] = value.strip()
            if not re.match(r"\s*[,}]", text[pos:]):
                raise ValueError("Expected comma or closing brace after " + name)
        entries.append(entry)
    return entries


def plain_text(value):
    value = value.replace(r"\&", "&").replace("~", " ")
    value = value.replace(r"\guillemotleft", "«").replace(r"\guillemotright", "»")
    return re.sub(r"\s+", " ", value.replace("{", "").replace("}", "")).strip()


def title_identity(value):
    value = unicodedata.normalize("NFKC", plain_text(value)).casefold()
    return "".join(char for char in value if char.isalnum())


def doi_identity(value):
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I).lower()


def dump_bibtex(entries):
    blocks = []
    for entry in entries:
        fields = ["  {} = {{{}}}".format(k, v) for k, v in entry.items()
                  if k not in ("entry_type", "bibtex_key") and v != ""]
        blocks.append("@{}{{{},\n{}\n}}".format(
            entry["entry_type"], entry["bibtex_key"], ",\n".join(fields)))
    return "\n\n".join(blocks) + "\n"


def merge_entries(local, incoming):
    """Local edits win; ORCID can add works and fill empty fields only."""
    merged = [dict(entry) for entry in local]
    for candidate in incoming:
        doi = doi_identity(candidate.get("doi", ""))
        title = title_identity(candidate["title"])
        match = next((entry for entry in merged if
                      (doi and doi == doi_identity(entry.get("doi", ""))) or
                      title == title_identity(entry["title"])), None)
        if match is not None:
            for key, value in candidate.items():
                if not match.get(key) and key not in ("bibtex_key", "entry_type"):
                    match[key] = value
        else:
            candidate = dict(candidate)
            used = {entry["bibtex_key"] for entry in merged}
            key = candidate["bibtex_key"]
            suffix = 2
            while candidate["bibtex_key"] in used:
                candidate["bibtex_key"] = "{}-{}".format(key, suffix)
                suffix += 1
            merged.append(candidate)
    return merged


def build_items(entries):
    keys, titles, dois = set(), set(), set()
    items = []
    types = {"article": "journal-article", "inproceedings": "conference-paper",
             "incollection": "book-chapter", "book": "book", "misc": "preprint",
             "phdthesis": "dissertation"}
    for entry in entries:
        key = entry["bibtex_key"]
        title = title_identity(entry.get("title", ""))
        doi = doi_identity(entry.get("doi", ""))
        if key in keys or title in titles or (doi and doi in dois):
            raise ValueError("Duplicate publication: " + key)
        keys.add(key)
        titles.add(title)
        if doi:
            dois.add(doi)
        if not title or not entry.get("author") or not re.fullmatch(r"\d{4}", entry.get("year", "")):
            raise ValueError("Missing title, authors or four-digit year: " + key)
        authors = []
        for author in re.split(r"\s+and\s+", entry["author"]):
            author = plain_text(author)
            if "," in author:
                family, given = (part.strip() for part in author.split(",", 1))
            else:
                parts = author.rsplit(" ", 1)
                given, family = parts if len(parts) == 2 else ("", parts[0])
            authors.append({"given": given, "family": family,
                            "full": (given + " " + family).strip()})
        entry_type = entry["entry_type"]
        category = entry.get("category") or (
            "conference" if entry_type == "inproceedings" else
            "thesis" if entry_type in ("phdthesis", "mastersthesis") else "publication")
        url = entry.get("url") or ("https://doi.org/" + doi if doi else "")
        item = {"key": doi or key, "bibtex_key": key,
                "title": plain_text(entry["title"]), "year": int(entry["year"]),
                "type": types.get(entry_type, entry_type), "entry_type": entry_type,
                "category": category, "venue": plain_text(entry.get("journal") or entry.get("booktitle", "")),
                "doi": doi, "url": url, "authors": authors}
        for field in ("volume", "number", "pages", "note", "code", "project", "slides", "dataset", "preprint"):
            item[field] = plain_text(entry.get(field, ""))
        item["paper"] = entry.get("paper") or url
        items.append(item)
    return sorted(items, key=lambda item: (-item["year"], item["title"].casefold()))


def write_views(root, entries):
    items = build_items(entries)
    payload = {"source_of_truth": "bibliography/publications.bib", "items": items}
    (root / "_data/publications.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    export = ["# Publications", "", "<!-- Generated from bibliography/publications.bib; do not edit here. -->", ""]
    for item in items:
        authors = ", ".join(author["full"] for author in item["authors"])
        line = "- {} ({}). **{}**. {}.".format(authors, item["year"], item["title"], item["venue"])
        if item["paper"]:
            line += " [Paper]({})".format(item["paper"])
        export.append(line)
    (root / "generated").mkdir(exist_ok=True)
    (root / "generated/publications.md").write_text("\n".join(export) + "\n", encoding="utf-8")
    return items
