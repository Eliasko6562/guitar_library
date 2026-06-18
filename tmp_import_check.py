import importlib, sys
try:
    importlib.import_module('library.models')
    print('import OK')
except Exception as e:
    print('IMPORT-ERROR', e)
    sys.exit(1)
