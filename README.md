# 🚀 JSON → CSV Converter for Sales Layer

A graphical tool that converts Sales Layer JSON exports into clean, structured CSV files suitable for analysis, migrations, or integration pipelines.

Supports both:

- **Simple JSON arrays** (BigCommerce‑style product lists)  
- **Full Sales Layer exports** (`data_schema` + `data` + any custom tables)

🔗 **Download Windows executable (.exe):**  
https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/json_to_csv_saleslayer_gui.exe

---

## ✨ Key Features

### ✔️ Automatic export of all tables

If the JSON contains tables like:

- `products`
- `product_formats`
- `catalogue`
- `mat_tabla_test`
- `custom_table_abc`
- *(any custom table created by the client)*

A CSV will be generated for each table:

```
products_1.csv
product_formats_1.csv
catalogue_1.csv
mat_tabla_test_1.csv
custom_table_abc_1.csv
```

---

### ✔️ Correct, collision‑free column names

Column names always match the original names in `data_schema`, including multilingual fields like:

```
name_en
name_es
name_fr
```

Never uses "sanitized" versions, avoiding name collisions.

---

### ✔️ Full compatibility with Sales Layer field types

Each field type is handled according to:

```json
data_schema_info[table][field].type
```

| SL Type  | CSV Behavior |
|----------|--------------|
| `string` | Clean text |
| `number` / `numeric` | Numeric value |
| `boolean` | True/False text |
| `list` | Comma‑separated |
| `image` | Extracts URLs (`ORG`) separated by ` | ` |
| `file`  | Extracts filenames separated by ` | ` |
| `table` | Embedded JSON |

---

### ✔️ Automatic size‑based file splitting

Choose the **maximum CSV file size (MB)**.  
Default: **19 MB**, adjustable in the interface.

If a table exceeds the limit:

```
products_1.csv
products_2.csv
products_3.csv
```

---

### ✔️ Automatic cleaning of HTML and line breaks

- HTML fields (like `body_html`) are flattened into a single line  
- Removes `
`, `
`, `	`  
- Proper CSV quoting applied  

---

### ✔️ Simple JSON array mode

If the JSON file looks like:

```json
[
  { "id": 1, "name": "...", "variants": [...] },
  { "id": 2, "name": "...", "variants": [...] }
]
```

The tool generates:

```
products_*.csv
variants_*.csv
categories_*.csv
```

---

## 🖥️ Graphical Interface

Includes:

- JSON file picker  
- Editable “Max file size (MB)”  
- Determinate progress bar  
- Real‑time log output  
- Clear error dialogs

<img width="780" height="608" alt="image" src="https://github.com/user-attachments/assets/4ef5ba47-8a9d-47f1-8fab-12698cf31340" />


---

# 📦 Install from source

Requirements:

- Python **3.8+**
- No external dependencies

Clone the project:

```bash
git clone https://github.com/Zafion/Conversor_Json-CSV_SalesLayer.git
cd Conversor_Json-CSV_SalesLayer
```

Run:

```bash
python json_to_csv_saleslayer_gui.py
```

---

# 🖥️ Download executable (.exe)

Download the latest version:

👉 https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/json_to_csv_saleslayer_gui.exe

Runs without installation.

---

# 🏗️ Build your own .exe with PyInstaller

Install:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed json_to_csv_saleslayer_gui.py
```

The executable appears in:

```
dist/json_to_csv_saleslayer_gui.exe
```

---

# 📁 Project Structure

```
Conversor_Json-CSV_SalesLayer/
├── json_to_csv_saleslayer_gui.py
├── json_to_csv_saleslayer_gui.exe   (optional)
└── README.md
```

---

# 🧪 Recommended testing

- Small/simple JSONs  
- Large Sales Layer exports  
- Custom tables (mat_*, custom_*, etc.)  
- HTML fields, images, files, lists, nested tables  

---

# ⚠️ Notes

- CSV files are generated in the **same folder** as the JSON  
- Large tables are automatically split  
- JSON input is never modified  

---

# 🤝 Contributing

Issues and PRs are welcome!

---

# 📄 License

MIT License — free to use, modify, and distribute.
