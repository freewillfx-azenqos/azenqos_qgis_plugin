import time

try:
    from qgis.core import QgsProject, QgsTask, QgsMessageLog, QgsRasterLayer, QgsRectangle, QgsLayerTreeLayer, QgsMapLayerType, QgsCoordinateReferenceSystem
except:
    pass


class LayerTask(QgsTask):
    def __init__(self, desc, databasePath, gc):
        QgsTask.__init__(self, desc)
        self.dbPath = databasePath
        self.start_time = None
        self.desc = desc
        self.exception = None
        self.vLayers = []
        self.gc = gc

    def addMapToQgis(self):
        # urlWithParams = 'type=xyz&url=http://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
        # urlWithParams = "type=xyz&url=http://ms.longdo.com/mmmap/img.php?zoom%3D%7Bz%7D%26x%3D%7Bx%7D%26y%3D%7By%7D%26mode%3Dicons%26key%3D93842be739d77f83f6b31c57ae56887f%26proj%3Depsg3857%26HD%3D1&zmax=18&zmin=0"

        urlWithParams = (
            "type=xyz&url=http://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png"
        )

        rlayer = QgsRasterLayer(urlWithParams, "Street map", "wms")
        if rlayer.isValid():
            QgsProject.instance().addMapLayer(rlayer)
            # self.azqGroup.addLayer(rlayer)
        else:
            QgsMessageLog.logMessage("Invalid layer")

    def zoomToActiveLayer(self):
        root = QgsProject.instance().layerTreeRoot()
        groups = root.findGroups()
        extent = QgsRectangle()
        extent.setMinimal()
        if len(groups) > 0:
            for child in groups[0].children():
                if isinstance(child, QgsLayerTreeLayer):
                    extent.combineExtentWith(child.layer().extent())
        else:
            layers = root.findLayers()
            for child in layers:
                if isinstance(child, QgsLayerTreeLayer):
                    msg = "child.layer().type(): {}".format(child.layer().type())
                    print(msg)
                    QgsMessageLog.logMessage(msg)
                    try:
                        if child.layer().type() == QgsMapLayerType.VectorLayer:
                            extent.combineExtentWith(child.layer().extent())
                    except Exception as ne:
                        print(
                            "check QgsMapLayerType.VectorLayer failed: {} - try fallback to alt method".format(
                                ne
                            )
                        )
                        if child.layer().type() == 0:
                            extent.combineExtentWith(child.layer().extent())

            self.gc.qgis_iface.mapCanvas().setExtent(extent)
            self.gc.qgis_iface.mapCanvas().refresh()

    def run(self):
        if not self.gc.qgis_iface:
            return
        QgsMessageLog.logMessage("[-- Start add layers --]", tag="Processing")
        self.start_time = time.time()
        return True

    def finished(self, result):
        if result:
            # gc.mostFeaturesLayer = None
            self.addMapToQgis()
            #geom_column = "geom"
            self.gc.qgis_iface.addVectorLayer(self.dbPath, None, "ogr")

            # Setting CRS
            my_crs = QgsCoordinateReferenceSystem(4326)
            QgsProject.instance().setCrs(my_crs)

            self.zoomToActiveLayer()

            elapsed_time = time.time() - self.start_time
            QgsMessageLog.logMessage(
                "Elapsed time: " + str(elapsed_time) + " s.", tag="Processing"
            )
            QgsMessageLog.logMessage("[-- End add layers --]", tag="Processing")
        else:
            if self.exception is None:
                QgsMessageLog.logMessage(
                    'Task "{name}" not successful but without '
                    "exception (probably the task was manually "
                    "canceled by the user)".format(name=self.desc),
                    tag="Exception",
                )
            else:
                QgsMessageLog.logMessage(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.desc,
                        exception=self.exception
                    ),
                    tag="Exception"
                )
                raise self.exception


class QuitTask(QgsTask):
    def __init__(self, desc, azenqosMain):
        QgsTask.__init__(self, desc)
        self.start_time = None
        self.desc = desc
        self.exception = None
        self.azqMain = azenqosMain

    def run(self):
        QgsMessageLog.logMessage(
            "[-- Start Removing Dependencies --]", tag="Processing"
        )
        self.start_time = time.time()
        return True

    def finished(self, result):
        if result:
            elapsed_time = time.time() - self.start_time
            QgsMessageLog.logMessage(
                "Elapsed time: " + str(elapsed_time) + " s.", tag="Processing"
            )
            QgsMessageLog.logMessage(
                "[-- End Removing Dependencies --]", tag="Processing"
            )
            """
            if self.azqMain.newImport is False:
                self.azqMain.databaseUi.removeMainMenu()
            """
        else:
            if self.exception is None:
                QgsMessageLog.logMessage(
                    'Task "{name}" not successful but without '
                    "exception (probably the task was manually "
                    "canceled by the user)".format(name=self.desc),
                    tag="Exception",
                )
            else:
                QgsMessageLog.logMessage(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.desc,
                        exception=self.exception
                    ),
                    tag="Exception"
                )
                raise self.exception
