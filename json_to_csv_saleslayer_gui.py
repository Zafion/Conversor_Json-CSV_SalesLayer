import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

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


def split_by_size(base_path, base_name, header, rows):
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

    for row in rows:
        row_with_newline = row + "\n"
        row_bytes = len(row_with_newline.encode("utf-8"))

        # si al añadir la fila nos pasamos del límite, guardamos archivo y empezamos otro
        if current_bytes + row_bytes > MAX_BYTES:
            save_file(file_index, current)
            file_index += 1
            current = header + row_with_newline
            current_bytes = len(current.encode("utf-8"))
        else:
            current += row_with_newline
            current_bytes += row_bytes

    # último archivo
    if current != header:
        save_file(file_index, current)


def process_json_file(json_path):
    # Carpeta destino = misma carpeta que el JSON
    base_path = os.path.dirname(json_path) or "."

    # Leer JSON
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"JSON inválido o no legible:\n{e}")
        return

    if not isinstance(data, list):
        messagebox.showerror("Error", "El JSON debe ser una lista de objetos (array).")
        return

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

    # Procesar los items igual que en el JS
    for item in data:
        # Producto
        ref = safe_ref(item.get("sku"), item.get("id"))
        name = safe_ref(item.get("name"), ref)
        desc = clean_description(item.get("description"))
        brand = (item.get("brand") or {}).get("name", "")
        images = ",".join(item.get("images", []))

        # categorías
        categories = item.get("categories", []) or []
        cat_refs = []
        for c in categories:
            name_cat = (c.get("name") or "").strip()
            if not name_cat:
                continue
            category_set.add(name_cat)
            cat_refs.append(name_cat.replace(" ", "_"))
        cats_str = ",".join(cat_refs)

        product_row = ",".join([
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
        ])
        product_rows.append(product_row)

        # Variantes
        variants = item.get("variants", []) or []
        for v in variants:
            variant_row = ",".join([
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
            ])
            variant_rows.append(variant_row)

    # Categorías
    category_rows = []
    for cat in sorted(category_set):
        ref_cat = cat.strip().replace(" ", "_")
        category_rows.append(
            f"{escape_csv(ref_cat)},{escape_csv(cat)},"
        )

    # Dividir y guardar
    split_by_size(base_path, "products", product_header, product_rows)
    split_by_size(base_path, "variants", variant_header, variant_rows)
    split_by_size(base_path, "categories", category_header, category_rows)

    messagebox.showinfo(
        "Hecho",
        "CSV creados y divididos correctamente (todos < 19MB)\n"
        f"Carpeta: {os.path.abspath(base_path)}"
    )


def select_file():
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo JSON",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        process_json_file(file_path)


def main():
    root = tk.Tk()
    root.title("JSON → CSV (dividido) para Sales Layer")

    root.geometry("500x200")

    label = tk.Label(
        root,
        text="Conversor JSON → CSV para Sales Layer\n"
             "Selecciona tu JSON y se generarán varios CSV (<19MB).",
        justify="center"
    )
    label.pack(pady=20)

    btn = tk.Button(root, text="Seleccionar JSON y convertir", command=select_file)
    btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
