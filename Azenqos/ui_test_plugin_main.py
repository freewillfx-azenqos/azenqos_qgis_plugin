from PyQt5.QtWidgets import QApplication

import azenqos_qgis_plugin


def test():
    app = QApplication([])
    print(app)
    azq = azenqos_qgis_plugin.azenqos_qgis_plugin(None)
    azq.run()


if __name__ == "__main__":
    test()
