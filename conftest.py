# этот файл нужен, чтобы pytest видел модули из корня проекта
# без него тесты не находят items.py, exchanges.py и т.д.

import sys
import os

# добавляем корневую папку проекта в пути поиска python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
