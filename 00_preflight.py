import importlib, sys
from pathlib import Path
print('=== SEMANA 12 · PRE-FLIGHT ===')
print('Python',sys.version.split()[0])
if sys.version_info < (3,10): print('ATENCAO: use Python >=3.10')
modulos=['fastapi','uvicorn','prometheus_client','sklearn','numpy','joblib','httpx','pytest','yaml']
falha=False
for m in modulos:
    try: mod=importlib.import_module(m); print(f'[OK] {m}: {getattr(mod,"__version__","instalado")}')
    except Exception as exc: print(f'[FALTA] {m}: {exc}'); falha=True
print('Pasta:',Path.cwd())
print('Etapa seguinte: python 01_treinar_modelo.py' if not falha else 'Execute: python -m pip install -r requirements.txt')
raise SystemExit(1 if falha else 0)
