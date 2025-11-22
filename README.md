# GROUP---5

# Financial Transactions Analysis Tool

## 🎯 Sprint Goal

Build a small, collaborative Python tool that:
- Reads the provided **Financial Transactions Dataset**,
- Cleans and validates the data,
- Produces simple **spending summaries**, **income/expense reports**, and **basic plots**,
- Exposes **clean, modular, documented functions** returning ready-to-use data/plot objects.

This repository was developed in a **one-week mini sprint** to practice Agile planning, collaboration, and Git workflows.

---

## 📂 Project Structure

```text
.
├─ data/
│   └─ transactions.csv           # (not tracked in git if large/sensitive)
├─ src/
│   ├─ __init__.py
│   ├─ io_utils.py                # data loading
│   ├─ cleaning.py                # cleaning & preprocessing
│   ├─ summary.py                 # income/expense, category, monthly summaries
│   └─ viz.py                     # plotting functions (return matplotlib figures)
├─ notebooks/
│   └─ demo_analysis.ipynb        # example usage of functions
├─ tests/
│   ├─ test_io_utils.py
│   ├─ test_cleaning.py
│   └─ test_summary.py
├─ .gitignore
└─ README.md

