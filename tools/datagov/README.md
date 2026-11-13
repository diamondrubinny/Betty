# data.gov.il → Betty knowledge base

Pulls three open datasets from data.gov.il and turns them into knowledge-base documents.

| Dataset | Publisher | Output |
|---|---|---|
| `regulationdatabase` (מאגר האסדרה) | רשות האסדרה | Index of safety and occupational-hygiene legislation, with links to full text |
| `mandatory-standards` (מאגר תקנים רשמיים) | משרד הכלכלה והתעשייה | List of official (mandatory) Israeli standards |
| `safetyorderslist` (רשימת צווי בטיחות) | משרד העבודה | Aggregated statistics of violated clauses (no site or company names) |

## Run

```bash
mkdir -p dg kbout
python3 tools/datagov/pull.py    # downloads raw rows into dg/*.json
python3 tools/datagov/build.py   # writes kbout/*.json (for the KB) and kbout/*.md
```

Both scripts use only the Python standard library and expect to run from a directory that contains `dg/`.

## Limits

- These datasets are indexes and statistics. They do not contain the wording of laws, regulations or standards.
- The legislation index links to full texts on he.wikisource.org; the standards' texts are copyrighted by the Standards Institution of Israel.
- Licence on data.gov.il: "Other (Open)". Terms of use should be verified before publication.
