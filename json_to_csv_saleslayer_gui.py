import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Valor por defecto en MB para el tamaño máximo de cada CSV
DEFAULT_MAX_MB = 19

# Textos ES / EN
TEXTS = {
    "es": {
        "window_title": "JSON → CSV (dividido) para Sales Layer",
        "description": (
            "Conversor JSON → CSV para Sales Layer\n"
            "• Formato simple: array de productos → products/variants/categories\n"
            "• Formato Sales Layer: genera un CSV por tabla "
            "(catalogue, products, product_formats, mat_*, etc.)."
        ),
        "button": "Seleccionar JSON y convertir",
        "size_label": "Tamaño máximo por archivo (MB):",
        "delim_label": "Delimitador CSV:",
        "lang_label": "Idioma:",
        "progress_label": "Progreso:",
        "log_label": "Log:",

        "err_size_title": "Error",
        "err_size_msg": "Introduce un tamaño válido en MB (por ejemplo: 5, 10, 19…).",

        "err_json_invalid": "JSON inválido o no legible: {error}",
        "err_json_format": (
            "No se ha reconocido el formato JSON.\n\n"
            "• Formato simple: la raíz debe ser un array de productos.\n"
            "• Formato Sales Layer: debe contener data_schema + data."
        ),

        "err_convert_title": "Error",
        "err_convert_saved": (
            "Ocurrió un error durante la conversión.\n\n"
            "Se ha guardado un archivo con el detalle en:\n{path}"
        ),
        "err_convert_nosave": (
            "Ocurrió un error durante la conversión y no se pudo guardar el archivo de log."
        ),

        "done_title": "Hecho",
        "done_msg": (
            "CSV creados y divididos correctamente\n"
            "(tamaño máximo: {mb} MB)\n"
            "Carpeta: {folder}"
        ),

        "log_start": "Iniciando conversión… (límite {mb} MB por archivo, delimitador '{delim}')",
        "log_opening": "Abriendo JSON: {path}",
        "log_simple_detected": "Detectado formato simple: array de productos en la raíz.",
        "log_saleslayer_detected": "Detectado JSON de Sales Layer (data_schema + data).",
        "log_processing_products": "Procesando {total} productos para generar CSV (modo simple)…",
        "log_processed_products": "Procesados {idx}/{total} productos (modo simple)…",
        "log_products_summary": (
            "Total filas productos: {prod}, variantes: {var}, categorías únicas: {cats}"
        ),
        "log_exporting_tables": "Exportando todas las tablas de Sales Layer (modo genérico)…",
        "log_table_nodata": "Tabla {table}: sin datos, se omite.",
        "log_table_rows": "Tabla {table}: {rows} filas.",
        "log_splitting_products": "Dividiendo y guardando products_*.csv…",
        "log_splitting_variants": "Dividiendo y guardando variants_*.csv…",
        "log_splitting_categories": "Dividiendo y guardando categories_*.csv…",
        "log_saving_file": "Guardado: {filename}",
        "log_finished": "Conversión terminada.",
        "log_error_read_json": "ERROR al leer JSON: {error}",
        "log_error_format": "ERROR: Formato JSON no reconocido.",

        "errfile_header": "=== Sales Layer JSON → CSV Converter ===\nConversión fallida.\n\n",
        "errfile_error_title": "=== Error ===\n",
        "errfile_log_title": "\n=== Log ===\n",
    },
    "en": {
        "window_title": "JSON → CSV (split) for Sales Layer",
        "description": (
            "JSON → CSV converter for Sales Layer\n"
            "• Simple format: product array → products/variants/categories\n"
            "• Sales Layer format: one CSV per table "
            "(catalogue, products, product_formats, mat_*, etc.)."
        ),
        "button": "Select JSON and convert",
        "size_label": "Max file size (MB):",
        "delim_label": "CSV delimiter:",
        "lang_label": "Language:",
        "progress_label": "Progress:",
        "log_label": "Log:",

        "err_size_title": "Error",
        "err_size_msg": "Please enter a valid size in MB (e.g. 5, 10, 19…).",

        "err_json_invalid": "Invalid or unreadable JSON: {error}",
        "err_json_format": (
            "JSON format not recognized.\n\n"
            "• Simple format: root must be an array of products.\n"
            "• Sales Layer format: must contain data_schema + data."
        ),

        "err_convert_title": "Error",
        "err_convert_saved": (
            "An error occurred during conversion.\n\n"
            "A log file has been saved at:\n{path}"
        ),
        "err_convert_nosave": (
            "An error occurred during conversion and the log file could not be saved."
        ),

        "done_title": "Done",
        "done_msg": (
            "CSV files created and split successfully\n"
            "(max size: {mb} MB)\n"
            "Folder: {folder}"
        ),

        "log_start": "Starting conversion… (limit {mb} MB per file, delimiter '{delim}')",
        "log_opening": "Opening JSON: {path}",
        "log_simple_detected": "Detected simple format: product array at root.",
        "log_saleslayer_detected": "Detected Sales Layer JSON (data_schema + data).",
        "log_processing_products": "Processing {total} products to generate CSV (simple mode)…",
        "log_processed_products": "Processed {idx}/{total} products (simple mode)…",
        "log_products_summary": (
            "Total product rows: {prod}, variants: {var}, unique categories: {cats}"
        ),
        "log_exporting_tables": "Exporting all Sales Layer tables (generic mode)…",
        "log_table_nodata": "Table {table}: no data, skipped.",
        "log_table_rows": "Table {table}: {rows} rows.",
        "log_splitting_products": "Splitting and saving products_*.csv…",
        "log_splitting_variants": "Splitting and saving variants_*.csv…",
        "log_splitting_categories": "Splitting and saving categories_*.csv…",
        "log_saving_file": "Saved: {filename}",
        "log_finished": "Conversion finished.",
        "log_error_read_json": "ERROR reading JSON: {error}",
        "log_error_format": "ERROR: JSON format not recognized.",

        "errfile_header": "=== Sales Layer JSON → CSV Converter ===\nConversion failed.\n\n",
        "errfile_error_title": "=== Error ===\n",
        "errfile_log_title": "\n=== Log ===\n",
    },
}


def clean_description(html):
    """Elimina comentarios <!-- --> de la descripción y hace trim."""
    if not html:
        return ""
    import re
    return re.sub(r"<!--[\s\S]*?-->", "", html).strip()


def safe_ref(value, fallback):
    """Si el valor es vacío o contiene un comentario HTML, usa el fallback."""
    if not value:
        return fallback
    if isinstance(value, str) and "<!--" in value:
        return fallback
    return value


def escape_csv(value):
    """Escapa un valor para CSV, eliminando saltos de línea y tabuladores."""
    if value is None:
        return '""'
    s = str(value)

    # Normalizar saltos de línea y tabuladores
    s = s.replace("\r\n", " ")
    s = s.replace("\n", " ")
    s = s.replace("\r", " ")
    s = s.replace("\t", " ")

    # Limpiar espacios extremos
    s = s.strip()

    # Escapar comillas dobles
    s = s.replace('"', '""')

    return f'"{s}"'


def split_by_size(
    base_path,
    base_name,
    header,
    rows,
    max_bytes,
    lang,
    log_fn=None,
    ui_update_fn=None,
):
    """
    Divide las filas en varios CSV de tamaño < max_bytes.
    base_path: ruta donde se guardan los ficheros
    base_name: nombre base de archivo (sin _n y sin .csv)
    header: string con la cabecera (terminado en \n)
    rows: lista de strings (cada row SIN \n)
    """
    texts = TEXTS.get(lang, TEXTS["es"])
    file_index = 1
    current = header
    current_bytes = len(current.encode("utf-8"))

    def save_file(index, content):
        filename = f"{base_name}_{index}.csv"
        full_path = os.path.join(base_path, filename)
        with open(full_path, "w", encoding="utf-8-sig", newline="") as f:
            f.write(content)
        if log_fn:
            log_fn(texts["log_saving_file"].format(filename=filename))

    for i, row in enumerate(rows, start=1):
        row_with_newline = row + "\n"
        row_bytes = len(row_with_newline.encode("utf-8"))

        if current_bytes + row_bytes > max_bytes:
            # Cerramos fichero actual y empezamos otro
            save_file(file_index, current)
            file_index += 1
            current = header + row_with_newline
            current_bytes = len(current.encode("utf-8"))
        else:
            current += row_with_newline
            current_bytes += row_bytes

        if ui_update_fn and i % 100 == 0:
            ui_update_fn()

    if current != header:
        save_file(file_index, current)


def save_error_log(log_text, error_message, json_path, lang="es"):
    """Guarda el log y el error en un archivo .txt al lado del JSON."""
    texts = TEXTS.get(lang, TEXTS["es"])
    try:
        base_path = os.path.dirname(json_path) or "."
        filename = "conversion_error_log.txt"
        full_path = os.path.join(base_path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(texts["errfile_header"])
            f.write(texts["errfile_error_title"])
            f.write(error_message + "\n")
            f.write(texts["errfile_log_title"])
            f.write(log_text or "")

        return full_path
    except Exception:
        return None


# ------------------------------------------------------------
#  MODO 1: JSON simple (array de productos tipo BigCommerce)
# ------------------------------------------------------------
def generate_csv_from_products(
    products,
    base_path,
    max_bytes,
    delimiter,
    lang,
    log_fn=None,
    ui_update_fn=None,
    progress_set_total=None,
    progress_step=None,
):
    """
    Motor original: array de objetos con campos id/name/sku/variants/categories…
    Genera products_X.csv, variants_X.csv, categories_X.csv.
    """
    texts = TEXTS.get(lang, TEXTS["es"])

    # Pre-cálculo de unidades de trabajo: productos + variantes + categorías
    num_products = len(products)
    num_variants = 0
    category_set_pre = set()

    for item in products:
        variants = item.get("variants", []) or []
        num_variants += len(variants)

        categories = item.get("categories", []) or []
        for c in categories:
            if isinstance(c, dict):
                name_cat = (c.get("name") or "").strip()
            else:
                name_cat = str(c).strip()
            if name_cat:
                category_set_pre.add(name_cat)

    num_categories = len(category_set_pre)
    total_units = num_products + num_variants + num_categories

    if progress_set_total and total_units > 0:
        progress_set_total(total_units)

    product_rows = []
    variant_rows = []
    category_set = set()

    product_header = (
        delimiter.join(
            [
                "reference",
                "name",
                "description",
                "brand",
                "price",
                "retail_price",
                "sale_price",
                "cost_price",
                "weight",
                "width",
                "height",
                "depth",
                "images",
                "category_references",
            ]
        )
        + "\n"
    )

    variant_header = (
        delimiter.join(
            [
                "variant_reference",
                "product_reference",
                "price",
                "retail_price",
                "sale_price",
                "cost_price",
                "weight",
                "width",
                "height",
                "depth",
                "upc",
                "inventory_level",
            ]
        )
        + "\n"
    )

    category_header = (
        delimiter.join(
            [
                "category_reference",
                "category_name",
                "parent_reference",
            ]
        )
        + "\n"
    )

    total_items = len(products)
    if log_fn:
        log_fn(texts["log_processing_products"].format(total=total_items))

    for idx, item in enumerate(products, start=1):
        ref = safe_ref(item.get("sku"), item.get("id"))
        name = safe_ref(item.get("name"), ref)
        desc = clean_description(item.get("description"))
        brand = (item.get("brand") or {}).get("name", "")
        images = ",".join(item.get("images", []))

        # categorías
        categories = item.get("categories", []) or []
        cat_refs = []
        for c in categories:
            if isinstance(c, dict):
                name_cat = (c.get("name") or "").strip()
            else:
                name_cat = str(c).strip()
            if not name_cat:
                continue
            category_set.add(name_cat)
            cat_refs.append(name_cat.replace(" ", "_"))
        cats_str = ",".join(cat_refs)

        product_row = delimiter.join(
            [
                escape_csv(ref),
                escape_csv(name),
                escape_csv(desc),
                escape_csv(brand),
                str(item.get("price", "") or ""),
                str(item.get("retail_price", "") or ""),
                str(item.get("sale_price", "") or ""),
                str(item.get("cost_price", "") or ""),
                str(item.get("weight", "") or ""),
                str(item.get("width", "") or ""),
                str(item.get("height", "") or ""),
                str(item.get("depth", "") or ""),
                escape_csv(images),
                escape_csv(cats_str),
            ]
        )
        product_rows.append(product_row)

        if progress_step:
            progress_step(1)

        # Variantes
        variants = item.get("variants", []) or []
        for v in variants:
            variant_row = delimiter.join(
                [
                    escape_csv(v.get("sku") or v.get("id") or ""),
                    escape_csv(ref),
                    str(v.get("price", "") or ""),
                    str(v.get("retail_price", "") or ""),
                    str(v.get("sale_price", "") or ""),
                    str(v.get("cost_price", "") or ""),
                    str(v.get("weight", "") or ""),
                    str(v.get("width", "") or ""),
                    str(v.get("height", "") or ""),
                    escape_csv(v.get("upc") or ""),
                    str(v.get("inventory_level", "") or ""),
                ]
            )
            variant_rows.append(variant_row)

            if progress_step:
                progress_step(1)

        if ui_update_fn and idx % 50 == 0:
            ui_update_fn()
            if log_fn:
                log_fn(
                    texts["log_processed_products"].format(
                        idx=idx, total=total_items
                    )
                )

    if log_fn:
        log_fn(
            texts["log_products_summary"].format(
                prod=len(product_rows),
                var=len(variant_rows),
                cats=len(category_set),
            )
        )

    # Categorías (usamos category_set_pre para no perder ninguna)
    category_rows = []
    for cat in sorted(category_set_pre):
        ref_cat = cat.strip().replace(" ", "_")
        category_rows.append(
            delimiter.join([escape_csv(ref_cat), escape_csv(cat), ""])
        )

        if progress_step:
            progress_step(1)

    if log_fn:
        log_fn(texts["log_splitting_products"])
    split_by_size(
        base_path,
        "products",
        product_header,
        product_rows,
        max_bytes,
        lang,
        log_fn,
        ui_update_fn,
    )

    if log_fn:
        log_fn(texts["log_splitting_variants"])
    split_by_size(
        base_path,
        "variants",
        variant_header,
        variant_rows,
        max_bytes,
        lang,
        log_fn,
        ui_update_fn,
    )

    if log_fn:
        log_fn(texts["log_splitting_categories"])
    split_by_size(
        base_path,
        "categories",
        category_header,
        category_rows,
        max_bytes,
        lang,
        log_fn,
        ui_update_fn,
    )


# ------------------------------------------------------------
#  MODO 2: JSON Sales Layer genérico (todas las tablas)
# ------------------------------------------------------------
def export_saleslayer_tables(
    raw,
    base_path,
    max_bytes,
    delimiter,
    lang,
    log_fn=None,
    ui_update_fn=None,
    progress_set_total=None,
    progress_step=None,
):
    """
    Recorre data_schema + data y crea un CSV por tabla:
    catalogue_X.csv, products_X.csv, product_formats_X.csv, mat_tabla_test_X.csv, etc.
    Usa TODOS los campos definidos en data_schema[tabla].
    """
    texts = TEXTS.get(lang, TEXTS["es"])
    data_schema = raw.get("data_schema", {})
    data = raw.get("data", {})
    schema_info = raw.get("data_schema_info", {})

    if log_fn:
        log_fn(texts["log_exporting_tables"])

    # Calcular total de filas (todas las tablas) para la barra de progreso
    total_rows = 0
    for table_name, schema_list in data_schema.items():
        rows = data.get(table_name)
        if isinstance(rows, list):
            total_rows += len(rows)

    if progress_set_total and total_rows > 0:
        progress_set_total(total_rows)

    for table_name, schema_list in data_schema.items():
        rows = data.get(table_name)
        if not isinstance(rows, list) or not rows:
            if log_fn:
                log_fn(texts["log_table_nodata"].format(table=table_name))
            continue

        if log_fn:
            log_fn(
                texts["log_table_rows"].format(
                    table=table_name, rows=len(rows)
                )
            )

        table_info = schema_info.get(table_name, {})
        headers = []
        col_meta = []
        used_headers = set()  # por compatibilidad, aunque ahora no lo necesitamos

        # Construimos cabeceras usando SIEMPRE el nombre original del campo
        for col in schema_list:
            if isinstance(col, str):
                key = col
            elif isinstance(col, dict):
                # { "images": [ ... ] } -> "images"
                key = list(col.keys())[0]
            else:
                key = "col"

            info = table_info.get(key, {})
            col_type = info.get("type")  # string, list, image, file, table, numeric…

            header_name = key  # siempre el nombre original
            used_headers.add(header_name)

            headers.append(escape_csv(header_name))
            col_meta.append((key, col_type))

        header_line = delimiter.join(headers) + "\n"

        # Función para transformar valor según tipo
        def transform_value(val, ctype):
            # Imagen: lista de [STATUS, ID, ORG]
            if ctype == "image":
                if isinstance(val, list):
                    urls = []
                    for elem in val:
                        if isinstance(elem, list) and len(elem) >= 3:
                            urls.append(str(elem[2]))
                    return " | ".join(urls)
                return ""
            # Ficheros: lista de [STATUS, ID, FILE]
            if ctype == "file":
                if isinstance(val, list):
                    files = []
                    for elem in val:
                        if isinstance(elem, list) and len(elem) >= 3:
                            files.append(str(elem[2]))
                    return " | ".join(files)
                return ""
            # Listas (tags, colecciones, etc.)
            if ctype == "list":
                if isinstance(val, list):
                    return ", ".join(str(v) for v in val)
                return str(val) if val not in (None, "") else ""
            # Tablas embebidas (ej: Equivalencias)
            if ctype == "table":
                try:
                    return json.dumps(val, ensure_ascii=False)
                except Exception:
                    return str(val)
            # Cualquier otra cosa -> texto plano
            return "" if val is None else str(val)

        # Construimos filas
        row_strings = []
        table_total_rows = len(rows)

        for r_idx, row in enumerate(rows, start=1):
            out_vals = []
            for i, (key, ctype) in enumerate(col_meta):
                val = row[i] if i < len(row) else None
                out_vals.append(escape_csv(transform_value(val, ctype)))
            row_strings.append(delimiter.join(out_vals))

            if progress_step:
                progress_step(1)

            if ui_update_fn and r_idx % 100 == 0:
                ui_update_fn()
                if log_fn:
                    log_fn(
                        f"{table_name}: {r_idx}/{table_total_rows} rows processed…"
                    )

        # Guardar/splitear CSV de esta tabla
        split_by_size(
            base_path,
            table_name,
            header_line,
            row_strings,
            max_bytes,
            lang,
            log_fn,
            ui_update_fn,
        )


# ------------------------------------------------------------
#  DETECCIÓN DE FORMATO + LÓGICA PRINCIPAL
# ------------------------------------------------------------
def process_json_file(
    json_path,
    log_fn=None,
    ui_update_fn=None,
    max_bytes=DEFAULT_MAX_MB * 1024 * 1024,
    delimiter=",",
    lang="es",
    progress_set_total=None,
    progress_step=None,
):
    base_path = os.path.dirname(json_path) or "."
    texts = TEXTS.get(lang, TEXTS["es"])

    if log_fn:
        log_fn(texts["log_opening"].format(path=json_path))

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        if log_fn:
            log_fn(texts["log_error_read_json"].format(error=e))
        # Propagamos para que select_file lo capture y genere el TXT
        raise Exception(texts["err_json_invalid"].format(error=e))

    # Caso 1: array simple de productos
    if isinstance(raw, list):
        if log_fn:
            log_fn(texts["log_simple_detected"])
        generate_csv_from_products(
            raw,
            base_path,
            max_bytes,
            delimiter,
            lang,
            log_fn,
            ui_update_fn,
            progress_set_total,
            progress_step,
        )

    # Caso 2: JSON de Sales Layer (data_schema + data)
    elif isinstance(raw, dict) and "data_schema" in raw and "data" in raw:
        if log_fn:
            log_fn(texts["log_saleslayer_detected"])
        export_saleslayer_tables(
            raw,
            base_path,
            max_bytes,
            delimiter,
            lang,
            log_fn,
            ui_update_fn,
            progress_set_total,
            progress_step,
        )

    else:
        if log_fn:
            log_fn(texts["log_error_format"])
        # Lanzamos excepción para que la GUI genere el log TXT
        raise Exception(texts["err_json_format"])

    mb_value = max_bytes // (1024 * 1024)
    messagebox.showinfo(
        texts["done_title"],
        texts["done_msg"].format(
            mb=mb_value, folder=os.path.abspath(base_path)
        ),
    )
    if log_fn:
        log_fn(texts["log_finished"])


# ------------------------------------------------------------
#  INTERFAZ GRÁFICA
# ------------------------------------------------------------
class JsonToCsvApp:
    def __init__(self, root):
        self.root = root

        # Idioma por defecto
        self.lang_var = tk.StringVar(value="EN")  # "ES" o "EN"

        self.root.geometry("800x600")

        # Frame superior (texto + botón)
        top_frame = tk.Frame(root)
        top_frame.pack(padx=10, pady=10, fill="x")

        self.label_description = tk.Label(
            top_frame,
            justify="left",
        )
        self.label_description.pack(side="left", padx=5)

        self.btn = tk.Button(
            top_frame,
            command=self.select_file,
        )
        self.btn.pack(side="right", padx=5)

        # Frame de opciones (tamaño + delimitador + idioma)
        options_frame = tk.Frame(root)
        options_frame.pack(padx=10, pady=(0, 5), fill="x")

        # Tamaño máximo (MB)
        self.size_label = tk.Label(options_frame)
        self.size_label.pack(side="left")
        self.size_var = tk.StringVar(value=str(DEFAULT_MAX_MB))  # valor por defecto
        self.size_entry = tk.Entry(options_frame, textvariable=self.size_var, width=6)
        self.size_entry.pack(side="left", padx=5)

        # Delimitador CSV
        self.delim_label = tk.Label(options_frame)
        self.delim_label.pack(side="left", padx=(20, 0))
        self.delim_var = tk.StringVar(value=",")
        self.delim_menu = ttk.Combobox(
            options_frame,
            textvariable=self.delim_var,
            width=8,
            state="readonly",
            values=[",", ";", "|", "TAB"],
        )
        self.delim_menu.pack(side="left", padx=5)

        # Idioma
        self.lang_label = tk.Label(options_frame)
        self.lang_label.pack(side="left", padx=(20, 0))
        self.lang_menu = ttk.Combobox(
            options_frame,
            textvariable=self.lang_var,
            width=5,
            state="readonly",
            values=["ES", "EN"],
        )
        self.lang_menu.pack(side="left", padx=5)
        self.lang_menu.bind("<<ComboboxSelected>>", self.on_lang_change)

        # Barra de progreso (modo determinate)
        progress_frame = tk.Frame(root)
        progress_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.progress_label = tk.Label(progress_frame)
        self.progress_label.pack(anchor="w")
        self.progress = ttk.Progressbar(progress_frame, mode="determinate")
        self.progress.pack(fill="x")

        # Caja de log
        log_frame = tk.Frame(root)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.log_label = tk.Label(log_frame)
        self.log_label.pack(anchor="w")

        self.log_text = tk.Text(log_frame, height=15, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Inicializar textos según idioma
        self.update_texts()

    # ---- utilidades idioma ----
    def get_lang_code(self):
        choice = self.lang_var.get().upper()
        return "en" if choice == "EN" else "es"

    def update_texts(self):
        lang = self.get_lang_code()
        texts = TEXTS.get(lang, TEXTS["es"])
        self.root.title(texts["window_title"])
        self.label_description.config(text=texts["description"])
        self.btn.config(text=texts["button"])
        self.size_label.config(text=texts["size_label"])
        self.delim_label.config(text=texts["delim_label"])
        self.lang_label.config(text=texts["lang_label"])
        self.progress_label.config(text=texts["progress_label"])
        self.log_label.config(text=texts["log_label"])

    def on_lang_change(self, event=None):
        self.update_texts()

    # ---- log & progreso ----
    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def get_full_log(self):
        return self.log_text.get("1.0", "end")

    def ui_pump(self):
        self.root.update_idletasks()
        self.root.update()

    def set_progress_total(self, total):
        """Configura el máximo de la barra de progreso."""
        total = max(int(total), 1)
        self.progress["maximum"] = total
        self.progress["value"] = 0
        self.ui_pump()

    def progress_step(self, step=1):
        """Avanza la barra de progreso."""
        self.progress.step(step)
        self.ui_pump()

    # ---- flujo principal ----
    def select_file(self):
        lang = self.get_lang_code()
        texts = TEXTS.get(lang, TEXTS["es"])

        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo JSON"
            if lang == "es"
            else "Select a JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        # Leer tamaño máximo en MB
        try:
            mb = float(self.size_var.get().replace(",", "."))
            if mb <= 0:
                raise ValueError
            max_bytes = int(mb * 1024 * 1024)
        except Exception:
            messagebox.showerror(
                texts["err_size_title"],
                texts["err_size_msg"],
            )
            return

        # Leer delimitador
        delim_choice = self.delim_var.get()
        if delim_choice == "TAB":
            delimiter = "\t"
        else:
            delimiter = delim_choice

        self.btn.config(state="disabled")
        self.progress["value"] = 0  # resetear barra
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.log(
            texts["log_start"].format(mb=mb, delim=delim_choice)
        )

        try:
            process_json_file(
                file_path,
                log_fn=self.log,
                ui_update_fn=self.ui_pump,
                max_bytes=max_bytes,
                delimiter=delimiter,
                lang=lang,
                progress_set_total=self.set_progress_total,
                progress_step=self.progress_step,
            )
        except Exception as e:
            error_msg = str(e)
            full_log = self.get_full_log()
            saved = save_error_log(full_log, error_msg, file_path, lang)

            if saved:
                messagebox.showerror(
                    texts["err_convert_title"],
                    texts["err_convert_saved"].format(path=saved),
                )
            else:
                messagebox.showerror(
                    texts["err_convert_title"],
                    texts["err_convert_nosave"],
                )
        finally:
            self.btn.config(state="normal")


def main():
    root = tk.Tk()
    app = JsonToCsvApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
