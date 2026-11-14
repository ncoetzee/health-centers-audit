# health-centers-audit

A Python toolkit for FQHC and nonprofit audit intelligence — automating data collection from federal government sources to support financial statement audit workflows.

## What This Does

This repository contains scripts built around auditing Federally Qualified Health Centers (FQHCs) and other nonprofit organizations subject to Single Audit / Uniform Guidance requirements. The core tool automates bulk download of Single Audit reports from the Federal Audit Clearinghouse (FAC), with supporting scripts for financial data extraction, ratio analysis, and UDS (Uniform Data System) spreadsheet construction.

## Key Scripts

| Script | Purpose |
|---|---|
| `fac_auto_downloader.py` | Bulk-downloads Single Audit PDFs from app.fac.gov using Playwright browser automation |
| `build_uds_spreadsheet.py` | Constructs UDS financial summary spreadsheets from extracted data |
| `download_pdfs.py` | Secondary PDF downloader via direct metadata links |
| `fetch_metadata.py` | Retrieves audit metadata from the FAC API |
| `api_explore.py` | Exploratory scripts for the FAC public API (swagger.json included) |
| `check_h80.py` / `inspect_h80.py` | Validates H80 grant data fields |
| `option1_pdf_parser.py` | PDF text extraction and parsing pipeline |

## Data Files

- `MA_FQHC_Financials_2023.csv` — Extracted financial data for Massachusetts FQHCs (2023)
- `fqhc_audits_ma.json` — Audit metadata for Massachusetts FQHCs
- `ma_fqhc_metadata.json` — HRSA metadata for Massachusetts FQHCs
- `fac_pdf_extracted_ratios.csv` — Financial ratios extracted from FAC audit PDFs

## Prerequisites

```bash
pip install playwright requests pandas
playwright install
```

## Usage

**Bulk download Single Audit PDFs from FAC:**
```bash
python fac_auto_downloader.py
```
Follow the on-screen prompts to enter search criteria on app.fac.gov before the script begins downloading.

## Context

The Federal Audit Clearinghouse (FAC) is the central repository for Single Audit reports under Uniform Guidance (2 CFR Part 200). FQHCs receiving federal funding (H80 grants, Medicaid, Medicare) above the $750,000 threshold are subject to Single Audit requirements. This toolkit supports auditors and researchers working in that space.

## Author

Nick Coetzee — Senior Auditor, AAFCPAs | [LinkedIn](https://www.linkedin.com/in/nicholascoetzee)
