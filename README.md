# JSON → CSV Converter for Sales Layer

<details>
<summary><strong>🇬🇧 English</strong></summary>

## 🚀 JSON → CSV Converter for Sales Layer

A graphical tool that converts Sales Layer JSON exports into clean, structured CSV files suitable for analysis, migrations, or integrations.

<img width="802" height="634" alt="image" src="https://github.com/user-attachments/assets/f0bc6da6-4c65-4392-bc44-e0ba52ece92f" />


Supports:

- **Simple JSON arrays** (BigCommerce‑style lists)
- **Full Sales Layer exports** (`data_schema`, `data`, custom tables, multilingual fields)

---

## 📦 Download Executables

Built automatically by GitHub Actions:

| Platform | Download |
|---------|----------|
| **Windows (.exe)** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-windows-latest.zip |
| **macOS** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-macos-latest.zip |
| **Linux** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-ubuntu-latest.zip |

---

## ✨ Features

### ✔️ Automatic JSON Format Detection  
- Simple JSON (array of products)  
- Sales Layer JSON (data_schema + data)

### ✔️ Multi‑language UI (NEW)  
The interface can switch between **English** and **Spanish**.

### ✔️ CSV Delimiter Selector (NEW)  
Choose: `,` • `;` • `|` • `TAB`.

### ✔️ Output File Size Limit (NEW)  
Split CSV files automatically when exceeding a user‑defined MB size.

### ✔️ Error Log Auto‑generation (NEW)  
If any error occurs, a file is created next to the JSON:

```
conversion_error_log.txt
```

Contains:
- Error message  
- Full on‑screen log  

### ✔️ Supports All Sales Layer Field Types  
Including: image arrays, file arrays, list fields, numeric, boolean, nested tables, and custom schemas.

### ✔️ Full Table Export  
Every table exported by Sales Layer is processed:

- products  
- product_formats  
- catalogue  
- mat_* tables  
- any custom table created by the client  

### ✔️ Safe CSV Formatting  
- Removes line breaks  
- Escapes quotes  
- Strips HTML comments  
- Prevents malformed CSV rows  

### ✔️ Determinate Progress Bar  
Reflects real row processing across all tables.

---

## 🖥️ Running from Source

```
python json_to_csv_saleslayer_gui.py
```

Dependencies: **Only Tkinter**, included in Python.

---

## 🏗️ Building Manually (Optional)

```
pip install pyinstaller
pyinstaller --onefile --windowed json_to_csv_saleslayer_gui.py
```

Result is in `dist/`.

---

## 🏭 GitHub Actions Auto‑Build

Three binaries are generated for:
- Windows  
- macOS  
- Linux  

They appear under:  
**Actions → Build desktop binaries → Artifacts**

---

## 🤝 Contributions  
Pull requests are welcome!

---

</details>

---

<details>
<summary><strong>🇪🇸 Español</strong></summary>

## 🚀 Conversor JSON → CSV para Sales Layer

Herramienta gráfica para convertir exportaciones JSON de Sales Layer en CSV limpios y estructurados para análisis, migraciones o integraciones.

<img width="802" height="634" alt="image" src="https://github.com/user-attachments/assets/2878473e-a208-402d-82b8-ac0ea475dd8b" />


Compatible con:

- **JSON simple** (listas de productos tipo BigCommerce)  
- **Exportaciones completas de Sales Layer** (`data_schema`, `data`, tablas personalizadas, campos por idioma)

---

## 📦 Descarga de ejecutables

Compilados automáticamente por GitHub Actions:

| Plataforma | Descarga |
|-----------|----------|
| **Windows (.exe)** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-windows-latest.zip |
| **macOS** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-macos-latest.zip |
| **Linux** | https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/app-ubuntu-latest.zip |

---

## ✨ Funcionalidades

### ✔️ Detección automática del tipo de JSON  
- JSON simple (array de productos)  
- JSON de Sales Layer (data_schema + data)

### ✔️ Interfaz multilenguaje (NUEVO)  
Cambia entre **inglés** y **español**.

### ✔️ Selector de delimitador CSV (NUEVO)  
Elige entre: `,` • `;` • `|` • `TAB`.

### ✔️ Tamaño máximo por archivo configurable (NUEVO)  
Divide automáticamente los CSV según el tamaño elegido por el usuario.

### ✔️ Generación automática de log de errores (NUEVO)  
Si ocurre un error se genera:

```
conversion_error_log.txt
```

Contiene:
- El mensaje de error  
- Todo el log mostrado en pantalla  

### ✔️ Soporta todos los tipos de campo de Sales Layer  
Incluye: imágenes, ficheros, listas, numéricos, booleanos, tablas anidadas y campos personalizados.

### ✔️ Exportación completa de tablas  
Cada tabla del JSON se exporta:

- products  
- product_formats  
- catalogue  
- mat_*  
- cualquier tabla personalizada  

### ✔️ Normalización segura del CSV  
- Elimina saltos de línea  
- Escapa comillas  
- Limpia comentarios HTML  
- Evita romper el CSV  

### ✔️ Barra de progreso real  
Basada en el conteo total de filas a procesar.

---

## 🖥️ Ejecutar desde el código fuente

```
python json_to_csv_saleslayer_gui.py
```

Dependencias: **solo Tkinter** (incluido con Python).

---

## 🏗️ Compilación manual (opcional)

```
pip install pyinstaller
pyinstaller --onefile --windowed json_to_csv_saleslayer_gui.py
```

El resultado aparece en `dist/`.

---

## 🏭 Compilación automática con GitHub Actions

Se generan ejecutables para:
- Windows  
- macOS  
- Linux  

Disponibles en:  
**Actions → Build desktop binaries → Artifacts**

---

## 🤝 Contribuciones  
¡Las PRs son bienvenidas!

---

</details>
