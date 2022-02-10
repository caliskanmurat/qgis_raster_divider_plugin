# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterDivider
                                 A QGIS plugin
 This plugin divides raster into equal sized parts.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-02-10
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Murat ÇALIŞKAN
        email                : caliskan.murat.20@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .raster_divider_dialog import RasterDividerDialog
import os.path

import os
from osgeo import gdal
from glob import glob
from qgis.core import QgsProject

class RasterDivider:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RasterDivider_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Raster Divider')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RasterDivider', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/raster_divider/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Raster Divider'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Raster Divider'),
                action)
            self.iface.removeToolBarIcon(action)
    
    
    def selectOutputFolder(self):
        self.dlg.le_outputFolder.setText("")
        self.output_dir = QFileDialog.getExistingDirectory(None, 'Open working directory', "", QFileDialog.ShowDirsOnly)
        self.dlg.le_outputFolder.setText(self.output_dir)
        
    def checkFolderPath(self):
        if  os.path.isdir(self.dlg.le_outputFolder.text()):
            self.dlg.lbl_message.setStyleSheet("color:black;")
            self.dlg.lbl_message.setText("")
        else:
            self.dlg.lbl_message.setStyleSheet("color:red; font-weight:bold;")
            self.dlg.lbl_message.setText("Invalid output folder path!")
    
    def getRasterSize(self):
        try:
            self.rasterName = self.rasterName = self.dlg.cb_in_raster.currentText()
            self.raster_path = self.raster_layers[self.rasterName].source()
            
            self.raster = gdal.Open(self.raster_path)        
            self.width = self.raster.RasterXSize
            self.height = self.raster.RasterYSize
            
            
            self.dlg.lbl_rasterWidth.setStyleSheet("color:black;")
            self.dlg.lbl_rasterHeight.setStyleSheet("color:black;")
            
            self.dlg.lbl_rasterWidth.setText(str(self.width))
            self.dlg.lbl_rasterHeight.setText(str(self.height))
            
            self.dlg.button_box.setEnabled(True)
            
        except:
            self.dlg.lbl_rasterWidth.setStyleSheet("color:red; font-weight:bold;")
            self.dlg.lbl_rasterHeight.setStyleSheet("color:red; font-weight:bold;")
            
            self.dlg.lbl_rasterWidth.setText("Invalid Raster!")
            self.dlg.lbl_rasterHeight.setText("Invalid Raster!")
            
            self.dlg.button_box.setEnabled(False)
       
    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            # self.first_start = False
            self.dlg = RasterDividerDialog()
            self.raster_layers = {layer.name():layer for layer in QgsProject.instance().mapLayers().values() if layer.type()== 1}
            self.dlg.cb_in_raster.clear()
            self.dlg.cb_in_raster.addItems(self.raster_layers.keys())
            self.getRasterSize()
            self.checkFolderPath()
            
            self.dlg.cb_in_raster.currentTextChanged.connect(self.getRasterSize)
            self.dlg.tb_browse.clicked.connect(self.selectOutputFolder)
            self.dlg.le_outputFolder.textChanged.connect(self.checkFolderPath)


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:            
            self.split_size_X = int(self.dlg.sb_rasterWidth.value())
            self.split_size_Y = int(self.dlg.sb_rasterHeight.value())
            self.out_folder = self.dlg.le_outputFolder.text()
            
            self.rasterName = self.rasterName = self.dlg.cb_in_raster.currentText()
            self.raster_path = self.raster_layers[self.rasterName].source()
            
            if not os.path.isdir(self.out_folder):
                QMessageBox.critical(None, "ERROR", "Invalid folder path!")                
            else:
                self.raster = gdal.Open(self.raster_path)
                self.crs = self.raster.GetSpatialRef()
                
                if not self.crs:
                    QMessageBox.critical(None, "ERROR", "Input raster does not have Coordinate Reference System!")
                    return
                    
                self.width = self.raster.RasterXSize
                self.height = self.raster.RasterYSize
                
                self.band = self.raster.GetRasterBand(1)
                self.noDataValue = self.band.GetNoDataValue()
                self.g1, self.g2, self.g3, self.g4, self.g5, self.g6 = self.raster.GetGeoTransform()
                
                if (self.width < self.split_size_X) or (self.height < self.split_size_Y):
                    QMessageBox.critical(None, "ERROR", "Width of chunk size must be lower than {} and height of chunk size must be lower than {}.".format(self.width+1, self.height+1))
                    return
                
                self.total_residual_X = (self.split_size_X - (self.width % self.split_size_X)) % self.split_size_X
                self.number_of_frame_X = int(self.width / self.split_size_X) if self.width % self.split_size_X == 0 else (self.width // self.split_size_X)+1
                
                self.total_residual_Y = (self.split_size_Y - (self.height % self.split_size_Y)) % self.split_size_Y
                self.number_of_frame_Y = int(self.height / self.split_size_Y) if self.height % self.split_size_Y == 0 else (self.height // self.split_size_Y)+1
                
                self.residual_X = self.total_residual_X // (self.number_of_frame_X - 1) if self.number_of_frame_X > 1 else 1
                self.residual_Y = self.total_residual_Y // (self.number_of_frame_Y - 1) if self.number_of_frame_Y > 1 else 1
                
                self.res_of_res_X = self.total_residual_X % (self.number_of_frame_X - 1) if self.number_of_frame_X > 1 else 1
                self.res_of_res_Y = self.total_residual_Y % (self.number_of_frame_Y - 1) if self.number_of_frame_Y > 1 else 1
                
                for fx in range(self.number_of_frame_X):
                    if fx == 0:
                        self.x0 = 0
                    else:
                        if fx < self.res_of_res_X + 1:
                            self.x0 = self.xend - self.residual_X - 1
                        else:
                            self.x0 = self.xend - self.residual_X
                    
                    self.xend = self.x0 + self.split_size_X
                    for fy in range(self.number_of_frame_Y):
                        if fy == 0:
                            self.y0 = 0
                        else:
                            if fy < self.res_of_res_Y + 1:
                                self.y0 = self.yend - self.residual_Y - 1
                            else:
                                self.y0 = self.yend - self.residual_Y
                        
                        self.yend = self.y0 + self.split_size_Y
                        
                        self.ng1 = self.g1 + self.x0 * self.g2
                        self.ng4 = self.g4 + self.y0 * self.g6
                        self.new_geot = (self.ng1, self.g2, self.g3, self.ng4, self.g5, self.g6)
                        
                        self.minX = self.ng1
                        self.maxY = self.ng4
                        self.maxX = self.minX + self.split_size_X * self.g2
                        self.minY = self.maxY + self.split_size_Y * self.g6
                        
                        self.raster_name = os.path.split(self.raster_path)[-1].split(".")[0]
                        self.name = "{}_{}_{}".format(self.raster_name, fx, fy)
                        self.newRasterSource = os.path.join(self.out_folder, self.name+".tif")
                        
                        self.out_raster = gdal.Warp(self.newRasterSource, self.raster, outputBounds=(self.minX, self.minY, self.maxX, self.maxY), dstNodata=self.noDataValue)
                        
                        del self.out_raster
            
            if self.dlg.chb_addToMap.isChecked():
                for p in glob(self.out_folder + r"\{}_[0-9]_[0-9].tif".format(self.raster_name)):
                    self.layer_name = os.path.split(p)[-1].split(".")[0]
                    iface.addRasterLayer(p, self.layer_name)
