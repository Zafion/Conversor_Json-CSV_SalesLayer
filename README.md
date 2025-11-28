# Conversor JSON → CSV para Sales Layer

**Conversor con interfaz gráfica que transforma JSONs de Sales Layer en CSVs listos para análisis, migraciones y conectores.**

Soporta tanto:

- **JSON simple** (array de productos tipo BigCommerce)
- **JSON completo de Sales Layer** (`data_schema` + `data` + tablas personalizadas)

🔗 **Descargar ejecutable (Windows .exe):**  
https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/json_to_csv_saleslayer_gui.exe

---

## Características principales

### ✔️ Exportación automática de todas las tablas

Si el JSON contiene tablas como:

- `products`
- `product_formats`
- `catalogue`
- `mat_tabla_test`
- `custom_table_abc`
- *(cualquier tabla creada por el cliente)*

Se generará un CSV por tabla:

```
products_1.csv
product_formats_1.csv
catalogue_1.csv
mat_tabla_test_1.csv
custom_table_abc_1.csv
```

---

### ✔️ Columnas correctas y sin duplicados

El conversor **siempre respeta los nombres reales** definidos en `data_schema`, incluso en campos multi-idioma:

```
denominacion_en
denominacion_es
denominacion_fr
```

Nunca usa `sanitized` (evita colisiones como "denominacion").

---

### ✔️ Compatibilidad total con tipos de Sales Layer

El tipo de cada columna viene definido por:

```json
data_schema_info[tabla][campo].type
```

La exportación se adapta automáticamente:

| Tipo SL  | Tratamiento en CSV |
|----------|--------------------|
| `string` | Texto limpio       |
| `number` / `numeric` | Número |
| `boolean` | Texto plano |
| `list` | Se convierte en una lista separada por comas |
| `image` | Exporta URLs (`ORG`) separadas por ` | ` |
| `file` | Exporta nombres de archivo separados por ` | ` |
| `table` | Exporta la estructura como JSON |

---

### ✔️ División automática por tamaño

Puedes elegir el **máximo de MB por archivo CSV**.  
Por defecto: **19 MB**, editable desde la interfaz.

Si una tabla excede el límite:

```
products_1.csv
products_2.csv
products_3.csv
```

---

### ✔️ Limpieza automática de HTML y saltos de línea

- Los campos como `body_html` se convierten a una sola línea.
- Se eliminan `
`, `
`, `	`.
- Se mantienen las comillas correctamente escapadas.

---

### ✔️ Modo productos simple (JSON array)

Si el archivo es:

```json
[
  { "id": 1, "name": "...", "variants": [...] },
  { "id": 2, "name": "...", "variants": [...] }
]
```

Produce:

```
products_*.csv
variants_*.csv
categories_*.csv
```

---

## Interfaz gráfica

Incluye:

- Selector de archivo JSON  
- Campo editable “Tamaño máximo por archivo (MB)”  
- Barra de progreso  
- Log en tiempo real  
- Alertas de error limpias

  <img width="791" height="580" alt="image" src="https://github.com/user-attachments/assets/8786a991-292c-47d7-b759-526487d6e707" />


---

# Instalación desde código fuente

Requisitos:

- Python **3.8+**
- Sin dependencias externas

Clonar el repositorio:

```bash
git clone https://github.com/Zafion/Conversor_Json-CSV_SalesLayer.git
cd Conversor_Json-CSV_SalesLayer
```

Ejecutar la aplicación:

```bash
python json_to_csv_saleslayer_gui.py
```

---

# Descargar ejecutable (.exe)

Haz clic aquí para descargar la última versión:

👉 https://raw.githubusercontent.com/Zafion/Conversor_Json-CSV_SalesLayer/refs/heads/main/json_to_csv_saleslayer_gui.exe

El `.exe` funciona sin instalación ni dependencias.

---

# Crear ejecutable .exe con PyInstaller

Instalar PyInstaller:

```bash
pip install pyinstaller
```

Empaquetar la app:

```bash
pyinstaller --onefile --windowed json_to_csv_saleslayer_gui.py
```

El ejecutable aparecerá en:

```
dist/json_to_csv_saleslayer_gui.exe
```

---

# Estructura del proyecto

```
Conversor_Json-CSV_SalesLayer/
├── json_to_csv_saleslayer_gui.py
├── json_to_csv_saleslayer_gui.exe    (opcional)
└── README.md
```

---

# Pruebas recomendadas

- JSONs pequeños y simples  
- JSONs grandes de Sales Layer  
- Tablas personalizadas (mat_*, custom_*, etc.)  
- Datos con HTML, imágenes, ficheros, listas, tablas anidadas

---

# Consideraciones

- Los CSV se generan en la **misma carpeta** que el JSON.
- Para datos muy grandes se creará más de un CSV por tabla.
- La exportación es idempotente: no modifica el JSON original.

---

# 🤝 Contribuir

¿Ideas, mejoras, bugs o nuevas funciones?  
Puedes abrir *issues* o enviar *pull requests*.

---

