# Job Posting Analyzer (AI-Assisted)

## Overview
A deterministic command-line tool that analyzes software job postings to:
- Detect technical skills using a curated, explainable keyword list
- Extract experience signals (years and seniority/entry keywords)
- Produce a conservative entry-level verdict (GO/NO-GO) with reasons

This project was built using a combination of manual development and AI-assisted coding tools (Cursor and ChatGPT), with a focus on validating and testing AI-generated output.

## Features
- Parse job descriptions from `.txt` files (file path input only)
- Extract technical skills (languages, frameworks, tools)
- Detect experience requirements and entry-level mismatches
- Output a structured analysis to the terminal

## Why This Project
This tool reflects a real workflow used by early-career engineers applying to software roles and demonstrates responsible use of generative AI in software development.

## Tech Stack
- Language: Python
- Interface: Command-line (CLI)
- Tools: Cursor, ChatGPT
- Version Control: Git / GitHub

## AI-Assisted Development Notes
AI tools were used to:
- Generate initial code scaffolding
- Assist with prompt design
- Suggest refactoring and improvements

All AI-generated code was reviewed, modified, and validated through testing.

## Status
MVP functionality implemented. Skill extraction and verdict logic are deterministic.

## Usage
From the project folder:

`python .\src\analyzer.py path\to\posting.txt`

Example:

`python .\src\analyzer.py .\data\sample_listings\job=posting-test.txt`

## Requirements
Python 3 must be installed on your machine to run the CLI.

## Sample Data
Sample listings are stored in the `data/sample_listings` folder.
