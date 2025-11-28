# Conversor_Json-CSV_SalesLayer
Conversor ejecutable con interfáz gráfica para convertir los Json de Sales Layer a CSV

Cómo convertirlo a ejecutable
En Windows con PyInstaller

Instalar PyInstaller (una sola vez):

En la terminal:
pip install pyinstaller


Desde la carpeta donde tengas json_to_csv_saleslayer_gui.py:

pyinstaller --onefile --windowed json_to_csv_saleslayer_gui.py


--onefile → un único .exe

--windowed → no se abre consola negra

El ejecutable aparecerá en la carpeta dist/
→ dist/json_to_csv_saleslayer_gui.exe
