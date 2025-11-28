import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Límite en bytes (19MB)
MAX_BYTES = 19 * 1024 * 1024


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
    """Escapa un valor para CSV (dobles comillas y envuelto en comillas)."""
    if value is None:
        return '""'
    s = str(value)
    s = s.replace('"', '""')
    return f'"{s}"'


def split_by_size(base_path, base_name, header, rows, log_fn=None, ui_update_fn=None):
    """
    Divide las filas en varios CSV de tamaño < MAX_BYTES.
    base_path: ruta donde se guardan los ficheros
    base_name: nombre base de archivo (sin _n y sin .csv)
    header: string con la cabecera (terminado en \n)
    rows: lista de strings (cada row SIN \n)
    """
    file_index = 1
    current = header
    current_bytes = len(current.encode("utf-8"))

    def save_file(index, content):
        filename = f"{base_name}_{index}.csv"
        full_path = os.path.join(base_path, filename)
        with open(full_path, "w", encoding="utf-8-sig", newline="") as f:
            f.write(content)
        if log_fn:
            log_fn(f"Guardado: {filename}")

    for i, row in enumerate(rows, start=1):
        row_with_newline = row + "\n"
        row_bytes = len(row_with_newline.encode("utf-8"))

        if current_bytes + row_bytes > MAX_BYTES:
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


# ------------------------------------------------------------
#  MODO 1: JSON simple (array de productos tipo BigCommerce)
# ------------------------------------------------------------
def generate_csv_from_products(products, base_path, log_fn=None, ui_update_fn=None):
    """
    Motor original: array de objetos con campos id/name/sku/variants/categories…
    Genera products_X.csv, variants_X.csv, categories_X.csv.
    """
    product_rows = []
    variant_rows = []
    category_set = set()

    product_header = (
        "reference,name,description,brand,price,retail_price,"
        "sale_price,cost_price,weight,width,height,depth,"
        "images,category_references\n"
    )

    variant_header = (
        "variant_reference,product_reference,price,retail_price,"
        "sale_price,cost_price,weight,width,height,depth,upc,"
        "inventory_level\n"
    )

    category_header = "category_reference,category_name,parent_reference\n"

    total_items = len(products)
    if log_fn:
        log_fn(f"Procesando {total_items} productos para generar CSV (modo simple)…")

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

        product_row = ",".join(
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

        # Variantes
        variants = item.get("variants", []) or []
        for v in variants:
            variant_row = ",".join(
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

        if ui_update_fn and idx % 50 == 0:
            ui_update_fn()
            if log_fn:
                log_fn(f"Procesados {idx}/{total_items} productos (modo simple)…")

    if log_fn:
        log_fn(f"Total filas productos: {len(product_rows)}")
        log_fn(f"Total filas variantes: {len(variant_rows)}")
        log_fn(f"Total categorías únicas: {len(category_set)}")

    # Categorías
    category_rows = []
    for cat in sorted(category_set):
        ref_cat = cat.strip().replace(" ", "_")
        category_rows.append(f"{escape_csv(ref_cat)},{escape_csv(cat)},")

    if log_fn:
        log_fn("Dividiendo y guardando products_*.csv…")
    split_by_size(base_path, "products", product_header, product_rows, log_fn, ui_update_fn)

    if log_fn:
        log_fn("Dividiendo y guardando variants_*.csv…")
    split_by_size(base_path, "variants", variant_header, variant_rows, log_fn, ui_update_fn)

    if log_fn:
        log_fn("Dividiendo y guardando categories_*.csv…")
    split_by_size(base_path, "categories", category_header, category_rows, log_fn, ui_update_fn)


# ------------------------------------------------------------
#  MODO 2: JSON Sales Layer genérico (todas las tablas)
# ------------------------------------------------------------
def export_saleslayer_tables(raw, base_path, log_fn=None, ui_update_fn=None):
    """
    Recorre data_schema + data y crea un CSV por tabla:
    catalogue_X.csv, products_X.csv, product_formats_X.csv, mat_tabla_test_X.csv, etc.
    Usa TODOS los campos definidos en data_schema[tabla].
    """
    data_schema = raw.get("data_schema", {})
    data = raw.get("data", {})
    schema_info = raw.get("data_schema_info", {})

    if log_fn:
        log_fn("Exportando todas las tablas de Sales Layer (modo genérico)…")

    for table_name, schema_list in data_schema.items():
        rows = data.get(table_name)
        if not isinstance(rows, list) or not rows:
            if log_fn:
                log_fn(f"Tabla {table_name}: sin datos, se omite.")
            continue

        if log_fn:
            log_fn(f"Tabla {table_name}: {len(rows)} filas.")

        # Construimos cabeceras usando sanitized si existe
        table_info = schema_info.get(table_name, {})
        headers = []
        col_meta = []  # guardamos (col_key, col_type) por índice

        for col in schema_list:
            if isinstance(col, str):
                key = col
            elif isinstance(col, dict):
                # { "images": [ ... ] } -> "images"
                key = list(col.keys())[0]
            else:
                key = "col"

            info = table_info.get(key, {})
            header_name = info.get("sanitized") or key  # p.e. id_catalogue / title / etc.
            col_type = info.get("type")  # string, list, image, file, table, numeric…
            headers.append(escape_csv(header_name))
            col_meta.append((key, col_type))

        header_line = ",".join(headers) + "\n"

        # Función para transformar valor según tipo
        def transform_value(val, ctype):
            # Imagen: lista de [STATUS, ID, ORG]
            if ctype == "image":
                if isinstance(val, list):
                    urls = []
                    for elem in val:
                        # elem: ["M","id","url"]
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
        total_rows = len(rows)

        for r_idx, row in enumerate(rows, start=1):
            out_vals = []
            for i, (key, ctype) in enumerate(col_meta):
                val = row[i] if i < len(row) else None
                out_vals.append(escape_csv(transform_value(val, ctype)))
            row_strings.append(",".join(out_vals))

            if ui_update_fn and r_idx % 100 == 0:
                ui_update_fn()
                if log_fn:
                    log_fn(f"Tabla {table_name}: procesadas {r_idx}/{total_rows} filas…")

        # Guardar/splitear CSV de esta tabla
        split_by_size(base_path, table_name, header_line, row_strings, log_fn, ui_update_fn)


# ------------------------------------------------------------
#  DETECCIÓN DE FORMATO + LÓGICA PRINCIPAL
# ------------------------------------------------------------
def process_json_file(json_path, log_fn=None, ui_update_fn=None):
    base_path = os.path.dirname(json_path) or "."

    if log_fn:
        log_fn(f"Abriendo JSON: {json_path}")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"JSON inválido o no legible:\n{e}")
        if log_fn:
            log_fn(f"ERROR al leer JSON: {e}")
        return

    # Caso 1: array simple de productos
    if isinstance(raw, list):
        if log_fn:
            log_fn("Detectado formato simple: array de productos en la raíz.")
        generate_csv_from_products(raw, base_path, log_fn, ui_update_fn)

    # Caso 2: JSON de Sales Layer (data_schema + data)
    elif isinstance(raw, dict) and "data_schema" in raw and "data" in raw:
        if log_fn:
            log_fn("Detectado JSON de Sales Layer (data_schema + data).")
        export_saleslayer_tables(raw, base_path, log_fn, ui_update_fn)

    else:
        messagebox.showerror(
            "Error",
            "No se ha reconocido el formato JSON.\n\n"
            "• Formato simple: la raíz debe ser un array de productos.\n"
            "• Formato Sales Layer: debe contener data_schema + data.",
        )
        if log_fn:
            log_fn("ERROR: Formato JSON no reconocido.")
        return

    messagebox.showinfo(
        "Hecho",
        "CSV creados y divididos correctamente (todos < 19MB)\n"
        f"Carpeta: {os.path.abspath(base_path)}",
    )
    if log_fn:
        log_fn("Conversión terminada.")


# ------------------------------------------------------------
#  INTERFAZ GRÁFICA
# ------------------------------------------------------------
class JsonToCsvApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON → CSV (dividido) para Sales Layer")
        self.root.geometry("750x520")

        # Frame superior (texto + botón)
        top_frame = tk.Frame(root)
        top_frame.pack(padx=10, pady=10, fill="x")

        label = tk.Label(
            top_frame,
            text=(
                "Conversor JSON → CSV para Sales Layer\n"
                "• Formato simple: array de productos → products/variants/categories\n"
                "• Formato Sales Layer: genera un CSV por tabla (catalogue, products, product_formats, mat_*, etc.)."
            ),
            justify="left",
        )
        label.pack(side="left", padx=5)

        self.btn = tk.Button(
            top_frame,
            text="Seleccionar JSON y convertir",
            command=self.select_file,
        )
        self.btn.pack(side="right", padx=5)

        # Barra de progreso
        progress_frame = tk.Frame(root)
        progress_frame.pack(padx=10, pady=(0, 10), fill="x")

        tk.Label(progress_frame, text="Progreso:").pack(anchor="w")
        self.progress = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress.pack(fill="x")

        # Caja de log
        log_frame = tk.Frame(root)
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(log_frame, text="Log:").pack(anchor="w")

        self.log_text = tk.Text(log_frame, height=15, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def ui_pump(self):
        self.root.update_idletasks()
        self.root.update()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if file_path:
            self.btn.config(state="disabled")
            self.progress.start(10)
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.config(state="disabled")
            self.log("Iniciando conversión...")
            try:
                process_json_file(
                    file_path, log_fn=self.log, ui_update_fn=self.ui_pump
                )
            finally:
                self.progress.stop()
                self.btn.config(state="normal")


def main():
    root = tk.Tk()
    app = JsonToCsvApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
