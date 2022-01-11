"""
This scripts goes through all QGIS projects and checks if they are valid.
It raises
"""


import qgis
from pathlib import Path
from qgis.core import QgsProject, QgsApplication, QgsErrorMessage
import os


PROJECTS_DIR = "/srv/projects"

def report_error(layer):
    # Implement custom error reporting here (sentry, logfile, etc...)
    pass

# Load PyQGIS
os.environ["QT_QPA_PLATFORM"]='offscreen'
QgsApplication.setPrefixPath("/usr/share/qgis/", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Iterate through all projects
exit_code = 0
project = QgsProject.instance()
for path in Path(PROJECTS_DIR).rglob("*.qgs"):
    abs_path = str(path.absolute())
    print(f"PROJECT {abs_path}")
    if not project.read(abs_path):
        print("Could not read project")
        continue
    # Iterate through all layers
    for layer in project.layerStore().mapLayers().values():
        print(f"  LAYER {layer.name()}...", end="")
        if not layer.isValid():
            exit_code = 1
            error = layer.error().message(format=QgsErrorMessage.Text) or "unknown error"
            print(f" ❌ ({error})")
            report_error(layer)
        else:
            print(" ✔️")

exit(exit_code)
