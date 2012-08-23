#!/usr/bin/env python

import gtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.artist import Artist
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.animation as animation
import tpmaker.tp_maker as tp

class GUI:
    
    def __init__(self):
        self.glade = gtk.Builder()
        self.glade.add_from_file('gui.glade')
        self.mainWindow = self.glade.get_object('mainWindow')
        self.mainWindow.show_all()
        
        self.glade.connect_signals(self)
        
        """
        WIDGETS DE VENTANAS DE DIALOGO
        """
        self.fileChooserDialog = gtk.FileChooserDialog("Cargar archivos binarios", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.fileChooserDialog.set_select_multiple(True)
        self.viewArrayDataDialog = self.glade.get_object('viewArrayDataDialog')
        self.viewArrayDataDialog.add_button("Cerrar", gtk.RESPONSE_CLOSE)
        self.aboutDialog = self.glade.get_object('aboutDialog')
        self.binaryFileErrorDialog = self.glade.get_object('binaryFileErrorDialog')
        
        self.menuViewArrayData = self.glade.get_object('menuViewArrayData')
        self.lstDatFiles = self.glade.get_object('lstDatFiles')
        self.lstArrayData = self.glade.get_object('lstArrayData')
        self.notebookVisualizationParams = self.glade.get_object('notebookVisualizationParams')
        
        """
        PARA GRAFICACION EN 1D
        """
        self.lstHorizontalAxis = self.glade.get_object('lstHorizontalAxis')
        self.lstVerticalAxis = self.glade.get_object('lstVerticalAxis')
        self.lblXPlane_1D = self.glade.get_object('lblXPlane_1D')
        self.lblYPlane_1D = self.glade.get_object('lblYPlane_1D')
        self.lblZPlane_1D = self.glade.get_object('lblZPlane_1D')
        self.spinXPlane_1D = self.glade.get_object('spinXPlane_1D')
        self.spinYPlane_1D = self.glade.get_object('spinYPlane_1D')
        self.spinZPlane_1D = self.glade.get_object('spinZPlane_1D')
        self.notebookCustomization1D = self.glade.get_object('notebookCustomization1D')
        self.txtTitleLabel1D = self.glade.get_object('txtTitleLabel1D')
        self.txtHorizontalAxisLabel = self.glade.get_object('txtHorizontalAxisLabel')
        self.txtVerticalAxisLabel = self.glade.get_object('txtVerticalAxisLabel')
        self.txtHorizontalAxisMinBound = self.glade.get_object('txtHorizontalAxisMinBound')
        self.txtHorizontalAxisMaxBound = self.glade.get_object('txtHorizontalAxisMaxBound')
        self.txtVerticalAxisMinBound = self.glade.get_object('txtVerticalAxisMinBound')
        self.txtVerticalAxisMaxBound = self.glade.get_object('txtVerticalAxisMaxBound')
        self.spinlineWidth = self.glade.get_object('spinLineWidth')
        self.lstLineStyle = self.glade.get_object('lstLineStyle')
        self.lstLineMarker = self.glade.get_object('lstLineMarker')
        self.lstLineMarkerFillStyle = self.glade.get_object('lstLineMarkerFillStyle')
        self.colorBackground = self.glade.get_object('colorBackground')
        self.checkGridX = self.glade.get_object('checkGridX')
        self.checkGridY = self.glade.get_object('checkGridY')
        
        """
        PARA GRAFICACION EN 2D
        """
        self.lstVariable2D = self.glade.get_object('lstVariable2D')
        self.lblXPlane_2D = self.glade.get_object('lblXPlane_2D')
        self.lblYPlane_2D = self.glade.get_object('lblYPlane_2D')
        self.lblZPlane_2D = self.glade.get_object('lblZPlane_2D')
        self.spinXPlane_2D = self.glade.get_object('spinXPlane_2D')
        self.spinYPlane_2D = self.glade.get_object('spinYPlane_2D')
        self.spinZPlane_2D = self.glade.get_object('spinZPlane_2D')
        self.notebookCustomization2D = self.glade.get_object('notebookCustomization2D')
        self.txtTitleLabel2D = self.glade.get_object('txtTitleLabel2D')
        self.checkEnableContourLines = self.glade.get_object('checkEnableContourLines')
        self.checkEnableContourLabels = self.glade.get_object('checkEnableContourLabels')
        self.checkEnableContourColorbar = self.glade.get_object('checkEnableContourColorbar')
        self.checkEnableContourFill = self.glade.get_object('checkEnableContourFill')
        self.checkEnableContourFillColorbar = self.glade.get_object('checkEnableContourFillColorbar')
        self.lstContourFillColorMap = self.glade.get_object('lstContourFillColorMap')
        self.countourSet2D = None
        self.levels = None
        self.im = None
        self.colorbarContour = None
        self.colorbarContourFill = None
        
        """
        PARA GRAFICACION EN 3D
        """
        self.lstVariable3D = self.glade.get_object('lstVariable3D')
        self.notebookCustomization3D = self.glade.get_object('notebookCustomization3D')
        
        """
        PARA ANIMACION EN 1D
        """
        self.lstHorizontalAxis_Animate = self.glade.get_object('lstHorizontalAxis_Animate')
        self.lstVerticalAxis_Animate = self.glade.get_object('lstVerticalAxis_Animate')
        self.lblXPlane_1D_Animate = self.glade.get_object('lblXPlane_1D_Animate')
        self.lblYPlane_1D_Animate = self.glade.get_object('lblYPlane_1D_Animate')
        self.lblZPlane_1D_Animate = self.glade.get_object('lblZPlane_1D_Animate')
        self.spinXPlane_1D_Animate = self.glade.get_object('spinXPlane_1D_Animate')
        self.spinYPlane_1D_Animate = self.glade.get_object('spinYPlane_1D_Animate')
        self.spinZPlane_1D_Animate = self.glade.get_object('spinZPlane_1D_Animate')

        """
        WIDGETS GENERALES
        """
        self.viewPort = self.glade.get_object('viewport')
        self.customizerPalette = self.glade.get_object('customizer')
        self.customizerPaletteTitle = self.glade.get_object('lblCustomizerTitle')
        
        self.label = self.glade.get_object('label4') #borrar luego, solo pruebas
        
        self.fig = Figure(figsize=(5,6), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.vbox = gtk.VBox(False, 2)
        self.vbox.pack_start(self.canvas)
        self.vbox.set_child_packing(self.canvas, True, True, 2, 0);
        self.container = gtk.Alignment(0.5,0.5,1.0,1.0)
        self.container.set_padding(3,5,5,5)
        self.container.add(self.vbox)
        self.viewPort.add(self.container)
        
        self.adjNX = None
        self.adjNY = None
        self.adjNZ = None
        self.adjLX = None
        self.adjLY = None
        self.adjLZ = None
        self.v1 = None
        self.v2 = None
        
        """
        WIDGETS Y VARIABLES GLOBALES
        """
        self.datSelection = self.lstDatFiles.get_selection()
        self.datSelection.set_mode(gtk.SELECTION_MULTIPLE)
        self.datSelection.connect('changed', self.selectFiles)
        self.listStore = gtk.ListStore(str,str)
        self.lstDatFiles.set_model(self.listStore)
        self.column = gtk.TreeViewColumn()
        self.lstDatFiles.append_column(self.column)
        self.render = gtk.CellRendererText()
        self.column.pack_start(self.render, True)
        self.column.add_attribute(self.render, 'text', 1)
        self.flagAddFiles = False
        
        self.listStoreAD = gtk.ListStore(int, float, float)
        self.lstArrayData.set_model(self.listStoreAD)
        
        self.column1 = gtk.TreeViewColumn("n")
        self.column1.set_alignment(0.5)
        self.column1.set_resizable(True)
        self.lstArrayData.append_column(self.column1)
        self.render1 = gtk.CellRendererText()
        self.column1.pack_start(self.render1, True)
        self.column1.add_attribute(self.render1, 'text', 0)
        
        self.column2 = gtk.TreeViewColumn("Abscisa")
        self.column2.set_alignment(0.5)
        self.column2.set_resizable(True)
        self.lstArrayData.append_column(self.column2)
        self.render2 = gtk.CellRendererText()
        self.column2.pack_start(self.render2, True)
        self.column2.add_attribute(self.render2, 'text', 1)
        
        self.column3 = gtk.TreeViewColumn("Ordenada")
        self.column3.set_alignment(0.5)
        self.column3.set_resizable(True)
        self.lstArrayData.append_column(self.column3)
        self.render3 = gtk.CellRendererText()
        self.column3.pack_start(self.render3, True)
        self.column3.add_attribute(self.render3, 'text', 2)

    def on_mainWindow_destroy(self, widget):
        gtk.main_quit()
        
    def openFileChooserDialog(self):
        filter = gtk.FileFilter()
        filter.set_name("Archivos binarios (.00x, .bin)")
        filter.add_pattern("*.bin")
        filter.add_pattern("*.00?")
        """
        self.fileChooserDialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Todos los Archivos")
        filter.add_pattern("*")
        """
        self.fileChooserDialog.add_filter(filter)
        response = self.fileChooserDialog.run()    
        if response == gtk.RESPONSE_OK:
            if self.flagAddFiles == False:
                self.listStore.clear()
                
            for i in self.fileChooserDialog.get_filenames():
                aux = True
                for j in self.lstDatFiles.get_model():
                    if j[0] == i:
                        aux = False
                if aux:
                    nameFile = i.split('/')
                    self.listStore.append([i,nameFile[-1]])
                
            self.fileChooserDialog.set_visible(False)
        
        elif response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
            self.fileChooserDialog.hide()
            
    def loadNumberNodes(self):
        try:
            tp.ini()
            nx = tp.dimensiones.nx
            ny = tp.dimensiones.ny
            nz = tp.dimensiones.nz
            self.adjNX = gtk.Adjustment(0.0, 0.0, float(nx-1), 1.0, 2.0, 0.0)
            self.adjNY = gtk.Adjustment(0.0, 0.0, float(ny-1), 1.0, 2.0, 0.0)
            self.adjNZ = gtk.Adjustment(0.0, 0.0, float(nz-1), 1.0, 2.0, 0.0)
            self.spinXPlane_1D.set_adjustment(self.adjNX)
            self.spinYPlane_1D.set_adjustment(self.adjNY)
            self.spinZPlane_1D.set_adjustment(self.adjNZ)
            self.spinXPlane_2D.set_adjustment(self.adjNX)
            self.spinYPlane_2D.set_adjustment(self.adjNY)
            self.spinZPlane_2D.set_adjustment(self.adjNZ)
        except:
            print "error"
            
        try:
            tp.leermalla()
            x = tp.mallagrid.x
            y = tp.mallagrid.y
            z = tp.mallagrid.z
            self.adjLX = gtk.Adjustment(0.0, 0.0, float(x[nx-1,0,0]), 1.0, 2.0, 0.0)
            self.adjLY = gtk.Adjustment(0.0, 0.0, float(y[0,ny-1,0]), 1.0, 2.0, 0.0)
            self.adjLZ = gtk.Adjustment(0.0, 0.0, float(z[0,0,nz-1]), 1.0, 2.0, 0.0)
        except:
            print "error"
    
    def on_menuFileLoadFiles_activate(self, widget):  
        self.openFileChooserDialog()
        
    def on_menuFileQuit_activate(self, widget):
        gtk.main_quit()
        
    def on_menuViewArrayData_activate(self, widget):
        self.listStoreAD.clear()  
        i = 0
        while i < np.size(self.v1):
            self.listStoreAD.append([i,self.v1[i],self.v2[i]])
            i = i + 1
        
        response = self.viewArrayDataDialog.run()
        if response == gtk.RESPONSE_CLOSE or response == gtk.RESPONSE_DELETE_EVENT:
            self.viewArrayDataDialog.hide()
        
    def on_menuAbout_activate(self, widget):
        response = self.aboutDialog.run()
        if response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
            self.aboutDialog.hide()
    
    def selectFiles(self,null=None):
        tree,iter = self.datSelection.get_selected_rows()
        self.datFiles = []
        
        for item in iter:
            self.datFiles.append(tree.get_value(tree.get_iter(item),0))
            
        if len(iter) == 1:
            self.notebookVisualizationParams.set_sensitive(True)
            self.notebookVisualizationParams.set_current_page(0)
            #self.notebookVisualizationParams.get_tab_label(self.notebookVisualizationParams.get_nth_page(1)).set_sensitive(False)
            self.notebookVisualizationParams.get_nth_page(0).set_sensitive(True)
            self.notebookVisualizationParams.get_nth_page(1).set_sensitive(False)
        elif len(iter) >= 2:
            self.notebookVisualizationParams.set_sensitive(True)
            self.notebookVisualizationParams.set_current_page(1)
            self.notebookVisualizationParams.get_nth_page(0).set_sensitive(False)
            self.notebookVisualizationParams.get_nth_page(1).set_sensitive(True)
        elif len(iter) == 0:
            self.notebookVisualizationParams.set_sensitive(False)
            
    def on_btnAddDatFile_clicked(self, widget):
        self.flagAddFiles = True
        self.openFileChooserDialog()
        
    def on_btnRemoveDatFile_clicked(self, widget):
        tree,iter = self.datSelection.get_selected_rows()
        i = len(iter)
        for item in iter:
            i = i - 1
            self.listStore.remove(tree.get_iter(iter[i]))
            
    """
    AQUI EMPIEZAN LOS PARAMETROS DE VISUALIZACION EN 1D
    """
    def loadVariables(self):
        self.listStoreHorizontalAxis_1D = gtk.ListStore(str)
        self.listStoreVerticalAxis_1D = gtk.ListStore(str)
        
        vars = ["X","Y","Z","U","V","W","P","T"]
        
        for i in vars[0:3]:
            self.listStoreHorizontalAxis_1D.append(i)
            
        for i in vars[3:8]:
            self.listStoreVerticalAxis_1D.append(i)
        
        self.lstHorizontalAxis.set_model(self.listStoreHorizontalAxis_1D)
        self.lstVerticalAxis.set_model(self.listStoreVerticalAxis_1D)
        
        self.lstHorizontalAxis.set_active(0)
        self.lstVerticalAxis.set_active(0)
        
        render = gtk.CellRendererText()
        self.lstHorizontalAxis.pack_start(render, True)
        self.lstHorizontalAxis.add_attribute(render, 'text', 0)
        self.lstVerticalAxis.pack_start(render, True)
        self.lstVerticalAxis.add_attribute(render, 'text', 0)
        
        self.listStoreVariable2D = gtk.ListStore(str)
            
        for i in vars[3:8]:
            self.listStoreVariable2D.append(i)
        
        self.lstVariable2D.set_model(self.listStoreVariable2D)
        
        self.lstVariable2D.set_active(0)
        
        render = gtk.CellRendererText()
        self.lstVariable2D.pack_start(render, True)
        self.lstVariable2D.add_attribute(render, 'text', 0)
        
        self.listStoreVariable3D = gtk.ListStore(str)
        
        for i in vars[3:8]:
            self.listStoreVariable3D.append(i)
            
        self.lstVariable3D.set_model(self.listStoreVariable3D)
        
        self.lstVariable3D.set_active(0)
        
        render = gtk.CellRendererText()
        self.lstVariable3D.pack_start(render, True)
        self.lstVariable3D.add_attribute(render, 'text', 0)
        

        self.listStoreHorizontalAxis_Animate = gtk.ListStore(str)
        self.listStoreVerticalAxis_Animate = gtk.ListStore(str)
        
        self.listStoreHorizontalAxis_Animate.clear()
        self.listStoreVerticalAxis_Animate.clear()
        
        for i in vars[0:3]:
            self.listStoreHorizontalAxis_Animate.append(i)
            
        for i in vars[3:8]:
            self.listStoreVerticalAxis_Animate.append(i)
        
        self.lstHorizontalAxis_Animate.set_model(self.listStoreHorizontalAxis_Animate)
        self.lstVerticalAxis_Animate.set_model(self.listStoreVerticalAxis_Animate)
        
        self.lstHorizontalAxis_Animate.set_active(0)
        self.lstVerticalAxis_Animate.set_active(0)
        
        render = gtk.CellRendererText()
        self.lstHorizontalAxis_Animate.pack_start(render, True)
        self.lstHorizontalAxis_Animate.add_attribute(render, 'text', 0)
        self.lstVerticalAxis_Animate.pack_start(render, True)
        self.lstVerticalAxis_Animate.add_attribute(render, 'text', 0)

    def on_lstHorizontalAxis_changed(self, widget):
        modelHAxis_1D = self.lstHorizontalAxis.get_model()
        selectedH = self.lstHorizontalAxis.get_active()
        
        if modelHAxis_1D[selectedH][0] == 'X':
            self.spinXPlane_1D.set_sensitive(False)
            self.spinYPlane_1D.set_sensitive(True)
            self.spinZPlane_1D.set_sensitive(True)
        elif modelHAxis_1D[selectedH][0] == 'Y':
            self.spinXPlane_1D.set_sensitive(True)
            self.spinYPlane_1D.set_sensitive(False)
            self.spinZPlane_1D.set_sensitive(True)
        elif modelHAxis_1D[selectedH][0] == 'Z':
            self.spinXPlane_1D.set_sensitive(True)
            self.spinYPlane_1D.set_sensitive(True)
            self.spinZPlane_1D.set_sensitive(False)
        else:
            self.spinXPlane_1D.set_sensitive(True)
            self.spinYPlane_1D.set_sensitive(True)
            self.spinZPlane_1D.set_sensitive(True)  
    
    def on_radioNodes_1D_toggled(self, widget):
        if widget.get_active:
            self.lblXPlane_1D.set_text("I:")
            self.lblYPlane_1D.set_text("J:")
            self.lblZPlane_1D.set_text("K:")
            self.spinXPlane_1D
            self.spinXPlane_1D.set_adjustment(self.adjNX)
            self.spinYPlane_1D.set_adjustment(self.adjNY)
            self.spinZPlane_1D.set_adjustment(self.adjNZ)
            
    def on_radioUnits_1D_toggled(self, widget):
        if widget.get_active:           
            self.lblXPlane_1D.set_text("X:")
            self.lblYPlane_1D.set_text("Y:")
            self.lblZPlane_1D.set_text("Z:")
            self.spinXPlane_1D.set_adjustment(self.adjLX)
            self.spinYPlane_1D.set_adjustment(self.adjLY)
            self.spinZPlane_1D.set_adjustment(self.adjLZ)
        
    def on_btnGraph1D_clicked(self, widget):
        self.viewPort.hide_all()
        modelHAxis_1D = self.lstHorizontalAxis.get_model()
        modelVAxis_1D = self.lstVerticalAxis.get_model()
        selectedH = self.lstHorizontalAxis.get_active()
        selectedV = self.lstVerticalAxis.get_active()
        
        #try:
        tp.main(self.datFiles[0])
        x = tp.mallagrid.x
        y = tp.mallagrid.y
        z = tp.mallagrid.z
        u = tp.velocidades.u
        v = tp.velocidades.v
        w = tp.velocidades.w
        p = tp.variables.p
        t = tp.variables.t
        
        if modelVAxis_1D[selectedV][0] == "U":
            if modelHAxis_1D[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(u[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(u[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = np.copy(u[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:])
                
        elif modelVAxis_1D[selectedV][0] == "V":
            if modelHAxis_1D[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(v[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(v[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = np.copy(v[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:])
                
        elif modelVAxis_1D[selectedV][0] == "W":
            if modelHAxis_1D[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(w[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(w[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = np.copy(w[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:])
                
        elif modelVAxis_1D[selectedV][0] == "P":
            if modelHAxis_1D[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(p[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(p[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = np.copy(p[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:])
                
        elif modelVAxis_1D[selectedV][0] == "T":
            if modelHAxis_1D[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(t[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = np.copy(t[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())])
            elif modelHAxis_1D[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = np.copy(t[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:])
        
        self.fig.clear()
        self.a = self.fig.add_subplot(111)
        self.a.set_xlabel(modelHAxis_1D[selectedH][0])
        self.a.set_ylabel(modelVAxis_1D[selectedV][0])
        self.a.set_title(modelHAxis_1D[selectedH][0] + ' vs ' + modelVAxis_1D[selectedV][0])
        self.a.plot(self.v1, self.v2)
        
        if len(self.vbox.get_children()) == 1:
            ntoolbar = NavigationToolbar(self.canvas, None)
            self.vbox.pack_end(ntoolbar)
            self.vbox.set_child_packing(ntoolbar, False, True, 2, 1)
        
        self.initCustomizationParams1D()
        
        self.viewPort.show_all()
        
        self.notebookCustomization1D.set_visible(True)
        self.notebookCustomization2D.set_visible(False)
        self.notebookCustomization3D.set_visible(False)
        self.customizerPalette.set_sensitive(True)
        self.menuViewArrayData.set_sensitive(True)
        
        tp.memoria_dealloc()
        """except:
            response = self.binaryFileErrorDialog.run()
            if response == gtk.RESPONSE_OK:
                self.binaryFileErrorDialog.hide()
"""
    """
    AQUI EMPIEZAN LOS PARAMETROS DE VISUALIZACION EN 2D
    """
    def on_radioNodes_2D_toggled(self, widget):
        if widget.get_active:
            self.lblXPlane_2D.set_text("I:")
            self.lblYPlane_2D.set_text("J:")
            self.lblZPlane_2D.set_text("K:")
            self.spinXPlane_2D.set_adjustment(self.adjNX)
            self.spinYPlane_2D.set_adjustment(self.adjNY)
            self.spinZPlane_2D.set_adjustment(self.adjNZ)
            
    def on_radioUnits_2D_toggled(self, widget):
        if widget.get_active:           
            self.lblXPlane_2D.set_text("X:")
            self.lblYPlane_2D.set_text("Y:")
            self.lblZPlane_2D.set_text("Z:")
            self.spinXPlane_2D.set_adjustment(self.adjLX)
            self.spinYPlane_2D.set_adjustment(self.adjLY)
            self.spinZPlane_2D.set_adjustment(self.adjLZ)
            
    def on_radioXPlane_toggled(self, widget):
        if widget.get_active:
            self.spinXPlane_2D.set_sensitive(True)
            self.spinYPlane_2D.set_sensitive(False)
            self.spinZPlane_2D.set_sensitive(False)
            
    def on_radioYPlane_toggled(self, widget):
        if widget.get_active:
            self.spinXPlane_2D.set_sensitive(False)
            self.spinYPlane_2D.set_sensitive(True)
            self.spinZPlane_2D.set_sensitive(False)

    def on_radioZPlane_toggled(self, widget):
        if widget.get_active:
            self.spinXPlane_2D.set_sensitive(False)
            self.spinYPlane_2D.set_sensitive(False)
            self.spinZPlane_2D.set_sensitive(True)
            
    def on_btnGraph2D_clicked(self, widget):
        self.viewPort.hide_all()
        modelVariable2D = self.lstVariable2D.get_model()
        selected = self.lstVariable2D.get_active()
        
        try:
            tp.main(self.datFiles[0])
            x = tp.mallagrid.x
            y = tp.mallagrid.y
            z = tp.mallagrid.z
            u = tp.velocidades.u
            v = tp.velocidades.v
            w = tp.velocidades.w
            p = tp.variables.p
            t = tp.variables.t
            
            if modelVariable2D[selected][0] == "U":
                if self.spinXPlane_2D.get_sensitive():
                    self.v1 = np.copy(u[int(self.spinXPlane_2D.get_value()),:,:])
                elif self.spinYPlane_2D.get_sensitive():
                    self.v1 = np.copy(u[:,int(self.spinYPlane_2D.get_value()),:])
                elif self.spinZPlane_2D.get_sensitive():
                    self.v1 = np.copy(u[:,:,int(self.spinZPlane_2D.get_value())])
    
            elif modelVariable2D[selected][0] == "V":
                if self.spinXPlane_2D.get_sensitive():
                    self.v1 = np.copy(v[int(self.spinXPlane_2D.get_value()),:,:])
                elif self.spinYPlane_2D.get_sensitive():
                    self.v1 = np.copy(v[:,int(self.spinYPlane_2D.get_value()),:])
                elif self.spinZPlane_2D.get_sensitive():
                    self.v1 = np.copy(v[:,:,int(self.spinZPlane_2D.get_value())])
                    
            elif modelVariable2D[selected][0] == "W":
                if self.spinXPlane_2D.get_sensitive():
                    self.v1 = np.copy(w[int(self.spinXPlane_2D.get_value()),:,:])
                elif self.spinYPlane_2D.get_sensitive():
                    self.v1 = np.copy(w[:,int(self.spinYPlane_2D.get_value()),:])
                elif self.spinZPlane_2D.get_sensitive():
                    self.v1 = np.copy(w[:,:,int(self.spinZPlane_2D.get_value())])
                    
            elif modelVariable2D[selected][0] == "P":
                if self.spinXPlane_2D.get_sensitive():
                    self.v1 = np.copy(p[int(self.spinXPlane_2D.get_value()),:,:])
                elif self.spinYPlane_2D.get_sensitive():
                    self.v1 = np.copy(p[:,int(self.spinYPlane_2D.get_value()),:])
                elif self.spinZPlane_2D.get_sensitive():
                    self.v1 = np.copy(p[:,:,int(self.spinZPlane_2D.get_value())])
                    
            elif modelVariable2D[selected][0] == "T":
                if self.spinXPlane_2D.get_sensitive():
                    self.v1 = np.copy(t[int(self.spinXPlane_2D.get_value()),:,:])
                elif self.spinYPlane_2D.get_sensitive():
                    self.v1 = np.copy(t[:,int(self.spinYPlane_2D.get_value()),:])
                elif self.spinZPlane_2D.get_sensitive():
                    self.v1 = np.copy(t[:,:,int(self.spinZPlane_2D.get_value())])

            self.fig.clear()
            self.a = self.fig.add_subplot(111)
            self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2))
            
            if np.min(self.v1) == np.max(self.v1):
                self.levels = np.arange(np.min(self.v1), np.max(self.v1), 0.0)
            else:
                self.levels = np.arange(np.min(self.v1), np.max(self.v1), np.std(self.v1))
    
            self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.jet)
            self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)
            self.a.set_title('Contorno de ' + modelVariable2D[selected][0])
            
            if len(self.vbox.get_children()) == 1:
                ntoolbar = NavigationToolbar(self.canvas, None)
                self.vbox.pack_end(ntoolbar)
                self.vbox.set_child_packing(ntoolbar, False, True, 2, 1)
            
            self.initCustomizationParams2D()
                
            self.viewPort.show_all()
            
            self.notebookCustomization1D.set_visible(False)
            self.notebookCustomization2D.set_visible(True)
            self.notebookCustomization3D.set_visible(False)
            self.customizerPalette.set_sensitive(True)
            self.menuViewArrayData.set_sensitive(True)
            
            tp.memoria_dealloc()
        except:
            response = self.binaryFileErrorDialog.run()
            if response == gtk.RESPONSE_OK:
                self.binaryFileErrorDialog.hide()
            
    """
    AQUI EMPIEZAN LOS PARAMETROS DE VISUALIZACION EN 3D
    """
    def on_btnGraph3D_clicked(self, widget):
        self.viewPort.hide_all()
        modelVariable3D = self.lstVariable3D.get_model()
        selected = self.lstVariable3D.get_active()
        
        #try:
        tp.main(self.datFiles[0])
        x = tp.mallagrid.x
        y = tp.mallagrid.y
        z = tp.mallagrid.z
        u = tp.velocidades.u
        v = tp.velocidades.v
        w = tp.velocidades.w
        p = tp.variables.p
        t = tp.variables.t
        
        
        self.v1 = np.copy(x[:,0,0])
        self.v2 = np.copy(y[0,:,0])
        v3 = np.copy(u[:,:,0])
        """
        for k in z:
            for j in y:
                for i in x:
                    v3 = u[]
        """
        
        self.fig.clear()
        #self.a = Axes3D(self.fig)
        self.a = self.fig.gca(projection='3d')
        X, Y = np.meshgrid(self.v1, self.v2)
        surface = self.a.plot_surface(X, Y, v3)
        self.a.set_zlim(0, 4)
        self.a.set_xlabel('X')
        self.a.set_ylabel('Y')
        self.a.set_zlabel('Z')
        
        #self.fig.colorbar(surface, shrink=0.5, aspect=5)
        
        if len(self.vbox.get_children()) == 1:
            ntoolbar = NavigationToolbar(self.canvas, None)
            self.vbox.pack_end(ntoolbar)
            self.vbox.set_child_packing(ntoolbar, False, True, 2, 1)
            
        self.viewPort.show_all()
        
        self.notebookCustomization1D.set_visible(False)
        self.notebookCustomization2D.set_visible(False)
        self.notebookCustomization3D.set_visible(True)
        self.customizerPalette.set_sensitive(True)
        self.menuViewArrayData.set_sensitive(True)
        
        tp.memoria_dealloc()
        """except:
            response = self.binaryFileErrorDialog.run()
            if response == gtk.RESPONSE_OK:
                self.binaryFileErrorDialog.hide()
            print "Fallo en lectura de archivo binario"
        """

    """
    AQUI EMPIEZAN LOS PARAMETROS DE ANIMACION EN 1D
    """ 
    def on_lstHorizontalAxis_Animate_changed(self, widget):
        modelHAxis = self.lstHorizontalAxis_Animate.get_model()
        selected = self.lstHorizontalAxis_Animate.get_active()
        
        if modelHAxis[selected][0] == 'X':
            self.spinXPlane_1D_Animate.set_sensitive(False)
            self.spinYPlane_1D_Animate.set_sensitive(True)
            self.spinZPlane_1D_Animate.set_sensitive(True)
        elif modelHAxis[selected][0] == 'Y':
            self.spinXPlane_1D_Animate.set_sensitive(True)
            self.spinYPlane_1D_Animate.set_sensitive(False)
            self.spinZPlane_1D_Animate.set_sensitive(True)
        elif modelHAxis[selected][0] == 'Z':
            self.spinXPlane_1D_Animate.set_sensitive(True)
            self.spinYPlane_1D_Animate.set_sensitive(True)
            self.spinZPlane_1D_Animate.set_sensitive(False)
        else:
            self.spinXPlane_1D_Animate.set_sensitive(True)
            self.spinYPlane_1D_Animate.set_sensitive(True)
            self.spinZPlane_1D_Animate.set_sensitive(True)  
    
    def on_radioNodes_1D_Animate_toggled(self, widget):
        if widget.get_active:
            self.lblXPlane_1D_Animate.set_text("I:")
            self.lblYPlane_1D_Animate.set_text("J:")
            self.lblZPlane_1D_Animate.set_text("K:")
            self.spinXPlane_1D_Animate.set_adjustment(self.adjNX)
            self.spinYPlane_1D_Animate.set_adjustment(self.adjNY)
            self.spinZPlane_1D_Animate.set_adjustment(self.adjNZ)
            
    def on_radioUnits_1D_Animate_toggled(self, widget):
        if widget.get_active:           
            self.lblXPlane_1D_Animate.set_text("X:")
            self.lblYPlane_1D_Animate.set_text("Y:")
            self.lblZPlane_1D_Animate.set_text("Z:")
            self.spinXPlane_1D_Animate.set_adjustment(self.adjLX)
            self.spinYPlane_1D_Animate.set_adjustment(self.adjLY)
            self.spinZPlane_1D_Animate.set_adjustment(self.adjLZ)
        
    def updateAnimation(self,file,line):
        modelHAxis = self.lstHorizontalAxis_Animate.get_model()
        modelVAxis = self.lstVerticalAxis_Animate.get_model()
        selectedH = self.lstHorizontalAxis_Animate.get_active()
        selectedV = self.lstVerticalAxis_Animate.get_active()
        
        tp.main(file)
        x = tp.mallagrid.x
        y = tp.mallagrid.y
        z = tp.mallagrid.z
        u = tp.velocidades.u
        v = tp.velocidades.v
        w = tp.velocidades.w
        p = tp.variables.p
        t = tp.variables.t
        
        if modelVAxis[selectedV][0] == "U":
            if modelHAxis[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = u[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = u[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = u[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                
        elif modelVAxis[selectedV][0] == "V":
            if modelHAxis[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = v[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = v[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = v[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                
        elif modelVAxis[selectedV][0] == "W":
            if modelHAxis[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = w[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = w[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = w[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                
        elif modelVAxis[selectedV][0] == "P":
            if modelHAxis[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = p[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = p[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = p[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                
        elif modelVAxis[selectedV][0] == "T":
            if modelHAxis[selectedH][0] == "X":
                self.v1 = x[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
                self.v2 = t[:,int(self.spinYPlane_1D.get_value()),int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Y":
                self.v1 = y[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
                self.v2 = t[int(self.spinXPlane_1D.get_value()),:,int(self.spinZPlane_1D.get_value())]
            elif modelHAxis[selectedH][0] == "Z":
                self.v1 = z[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
                self.v2 = t[int(self.spinXPlane_1D.get_value()),int(self.spinYPlane_1D.get_value()),:]
        
        tp.memoria_dealloc()
        
        line.set_xdata(self.v1)
        line.set_ydata(self.v2)
        
        return line,

    def on_btnAnimate1D_clicked(self, widget):
        self.viewPort.hide_all()        
        #try:
        self.fig.clear()
        for file in self.datFiles:
            self.a = self.fig.add_subplot(111)
            """self.a.set_xlabel(modelHAxis[selectedH][0])
            self.a.set_ylabel(modelVAxis[selectedV][0])
            self.a.set_title(modelHAxis[selectedH][0] + ' vs ' + modelVAxis[selectedV][0])"""
            #self.a.plot(self.v1, self.v2)
    
            line, = self.a.plot(self.v1, self.v2)
            
            ani = animation.FuncAnimation(self.fig, self.updateAnimation(file, line), 3, interval=1000)              
            
            if len(self.vbox.get_children()) == 1:
                ntoolbar = NavigationToolbar(self.canvas, None)
                self.vbox.pack_end(ntoolbar)
                self.vbox.set_child_packing(ntoolbar, False, True, 2, 1)
            
            self.viewPort.show_all()
            
            self.txtTitleLabel.set_text(self.a.get_title())
            self.txtHorizontalAxisLabel.set_text(self.a.get_xlabel())
            self.txtHorizontalAxisMinBound.set_text(str(self.a.get_xbound()[0]))
            self.txtHorizontalAxisMaxBound.set_text(str(self.a.get_xbound()[1]))
            self.txtVerticalAxisLabel.set_text(self.a.get_ylabel())
            self.txtVerticalAxisMinBound.set_text(str(self.a.get_ybound()[0]))
            self.txtVerticalAxisMaxBound.set_text(str(self.a.get_ybound()[1]))
            
            self.customizerPalette.set_sensitive(True)
            self.menuViewArrayData.set_sensitive(True)
        
        #except:
            #print "Fallo en lectura de archivo binario"    

    """
    AQUI EMPIEZAN LOS PARAMETROS DE PERSONALIZACION DE LAS GRAFICAS EN 1D
    """
    def initCustomizationParams1D(self):
        self.txtTitleLabel1D.set_text(self.a.get_title())
        self.txtHorizontalAxisLabel.set_text(self.a.get_xlabel())
        self.txtHorizontalAxisMinBound.set_text(str(self.a.get_xbound()[0]))
        self.txtHorizontalAxisMaxBound.set_text(str(self.a.get_xbound()[1]))
        self.txtVerticalAxisLabel.set_text(self.a.get_ylabel())
        self.txtVerticalAxisMinBound.set_text(str(self.a.get_ybound()[0]))
        self.txtVerticalAxisMaxBound.set_text(str(self.a.get_ybound()[1]))
        
        listStoreMarkers = gtk.ListStore(str, str)
        for k, v in Line2D.markers.iteritems():
            if type(k) == str and k != '' and k != ' ':
                listStoreMarkers.append([str(k) + " " + str(v), str(k)])
        if self.lstLineMarker.get_model() is None:
            self.lstLineMarker.set_model(listStoreMarkers)
            self.lstLineMarker.set_active(3)
            render = gtk.CellRendererText()
            self.lstLineMarker.pack_start(render, True)
            self.lstLineMarker.add_attribute(render, 'text', 0)
            
        listStoreLineStyle = gtk.ListStore(str, str)
        for k, v in Line2D.lineStyles.iteritems():
            if k != '' and k != ' ':
                listStoreLineStyle.append([str(k) + " " + str(v), str(k)])
        if self.lstLineStyle.get_model() is None:
            self.lstLineStyle.set_model(listStoreLineStyle)
            self.lstLineStyle.set_active(3)
            render = gtk.CellRendererText()
            self.lstLineStyle.pack_start(render, True)
            self.lstLineStyle.add_attribute(render, 'text', 0)
        
        listStoreLineMarkerFillStyle = gtk.ListStore(str)
        for i in Line2D.fillStyles:
            listStoreLineMarkerFillStyle.append([i])
        if self.lstLineMarkerFillStyle.get_model() is None:
            self.lstLineMarkerFillStyle.set_model(listStoreLineMarkerFillStyle)
            self.lstLineMarkerFillStyle.set_active(0)
            render = gtk.CellRendererText()
            self.lstLineMarkerFillStyle.pack_start(render, True)
            self.lstLineMarkerFillStyle.add_attribute(render, 'text', 0)
        
        self.checkGridX.set_active(False)
        self.checkGridY.set_active(False)
        
    def on_customizer_activate(self, widget):
        if self.customizerPalette.get_expanded():
            self.customizerPaletteTitle.set_angle(90)
        else:
            self.customizerPaletteTitle.set_angle(0)
            
    def on_txtTitleLabel1D_changed(self, widget):
        self.a.set_title(self.txtTitleLabel1D.get_text())
        self.fig.canvas.draw()
        
    def on_txtHorizontalAxisLabel_changed(self, widget):
        self.a.set_xlabel(self.txtHorizontalAxisLabel.get_text())
        self.fig.canvas.draw()
        
    def on_txtVerticalAxisLabel_changed(self, widget):
        self.a.set_ylabel(self.txtVerticalAxisLabel.get_text())
        self.fig.canvas.draw()
        
    def on_txtHorizontalAxisMinBound_changed(self, widget):
        if self.txtHorizontalAxisMinBound.get_text() != "" and self.txtHorizontalAxisMinBound.get_text() != "-" and self.txtHorizontalAxisMinBound.get_text() != "+":
            self.a.set_xbound(float(self.txtHorizontalAxisMinBound.get_text()), None)
            self.fig.canvas.draw()
        
    def on_txtHorizontalAxisMaxBound_changed(self, widget):
        if self.txtHorizontalAxisMaxBound.get_text() != "" and self.txtHorizontalAxisMaxBound.get_text() != "-" and self.txtHorizontalAxisMaxBound.get_text() != "+":
            self.a.set_xbound(None, float(self.txtHorizontalAxisMaxBound.get_text()))
            self.fig.canvas.draw()
        
    def on_txtVerticalAxisMinBound_changed(self, widget):
        if self.txtVerticalAxisMinBound.get_text() != "" and self.txtVerticalAxisMinBound.get_text() != "-" and self.txtVerticalAxisMinBound.get_text() != "+":
            self.a.set_ybound(float(self.txtVerticalAxisMinBound.get_text()), None)
            self.fig.canvas.draw()

    def on_txtVerticalAxisMaxBound_changed(self, widget):
        if self.txtVerticalAxisMaxBound.get_text() != "" and self.txtVerticalAxisMaxBound.get_text() != "-" and self.txtVerticalAxisMaxBound.get_text() != "+":
            self.a.set_ybound(None, float(self.txtVerticalAxisMaxBound.get_text()))
            self.fig.canvas.draw()
        
    def on_colorLine_color_set(self, widget):
        self.color = widget.get_color()
        
        r = (float(self.color.red) / 256.0) / 256.0
        g = (float(self.color.green) / 256.0) / 256.0
        b = (float(self.color.blue) / 256.0) / 256.0
    
        line, = self.a.get_lines()
        line.set_color([r,g,b])
        
        self.fig.canvas.draw()
        
    def on_spinLineWidth_value_changed(self, widget):
        line, = self.a.get_lines()
        line.set_linewidth(self.spinlineWidth.get_value())
        self.fig.canvas.draw()

    def on_lstLineStyle_changed(self, widget):
        model = self.lstLineStyle.get_model()
        selected = self.lstLineStyle.get_active()
        
        line, = self.a.get_lines()
        line.set_linestyle(model[selected][1])
        self.fig.canvas.draw()  
    
    def on_lstLineMarker_changed(self, widget):
        model = self.lstLineMarker.get_model()
        selected = self.lstLineMarker.get_active()
        
        line, = self.a.get_lines()
        line.set_marker(model[selected][1])
        self.fig.canvas.draw()
        
    def on_lstLineMarkerFillStyle_changed(self, widget):
        model = self.lstLineMarkerFillStyle.get_model()
        selected = self.lstLineMarkerFillStyle.get_active()
        
        line, = self.a.get_lines()
        line.set_fillstyle(model[selected][0])
        self.fig.canvas.draw()
    
    def on_colorLineMarker_color_set(self, widget):
        self.color = widget.get_color()
        
        r = (float(self.color.red) / 256.0) / 256.0
        g = (float(self.color.green) / 256.0) / 256.0
        b = (float(self.color.blue) / 256.0) / 256.0
        
        line, = self.a.get_lines()
        line.set_markerfacecolor([r,g,b])
        self.fig.canvas.draw()
        
    def on_spinLineMarkerSize_value_changed(self, widget):
        line, = self.a.get_lines()
        line.set_markersize(widget.get_value())
        self.fig.canvas.draw()
        
    def on_colorBackground_color_set(self, widget):
        self.color = self.colorBackground.get_color()
        
        r = (float(self.color.red) / 256.0) / 256.0
        g = (float(self.color.green) / 256.0) / 256.0
        b = (float(self.color.blue) / 256.0) / 256.0
        
        self.a.set_axis_bgcolor([r,g,b])
        self.fig.canvas.draw()
        
    def on_checkGridX_toggled(self, widget):
        if widget.get_active():
            self.a.grid(b=True, which='major', axis='x')
            self.fig.canvas.draw()
        else:
            self.a.grid(b=False)
            self.fig.canvas.draw()
            
    def on_checkGridY_toggled(self, widget):
        if widget.get_active():
            self.a.grid(b=True, which='major', axis='y')
            self.fig.canvas.draw()
        else:
            self.a.grid(b=False)
            self.fig.canvas.draw()
            
    """
    AQUI EMPIEZAN LOS PARAMETROS DE PERSONALIZACION DE LAS GRAFICAS EN 2D
    """
    def initCustomizationParams2D(self):
        self.txtTitleLabel2D.set_text(self.a.get_title())
        
        colormaps = ['jet','autumn','bone','cool','copper','flag','gray','hot','hsv','pink','prism','spring','summer','winter','spectral']
        listStoreContourFillColormap = gtk.ListStore(str)
        for i in colormaps:
            listStoreContourFillColormap.append([i])
        if self.lstContourFillColorMap.get_model() is None:
            self.lstContourFillColorMap.set_model(listStoreContourFillColormap)
            self.lstContourFillColorMap.set_active(0)
            render = gtk.CellRendererText()
            self.lstContourFillColorMap.pack_start(render, True)
            self.lstContourFillColorMap.add_attribute(render, 'text', 0)
        
    def on_txtTitleLabel2D_changed(self, widget):
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()
        
    def on_checkEnableContourLines_toggled(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active() 
        if widget.get_active():
            self.fig.clear()
            self.a = self.fig.add_subplot(111)    
            self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
            if self.checkEnableContourLabels.get_active():
                self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
            if self.checkEnableContourColorbar.get_active():
                self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
            if self.checkEnableContourFill.get_active():
                self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
                if self.checkEnableContourFillColorbar.get_active():
                    self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)            
            self.checkEnableContourLabels.set_sensitive(True)
            self.checkEnableContourColorbar.set_sensitive(True)
        else:
            self.a.clear()
            self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
            self.checkEnableContourLabels.set_sensitive(False)
            self.checkEnableContourColorbar.set_sensitive(False)
            self.checkEnableContourFill.set_active(True)
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()
        
    def on_checkEnableContourLabels_toggled(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active()
        if widget.get_active():
            self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
        else:
            self.fig.clear()
            self.a = self.fig.add_subplot(111)
            if self.checkEnableContourFill.get_active():
                self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
                if self.checkEnableContourFillColorbar.get_active():
                    self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)
            self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
            if self.checkEnableContourColorbar.get_active():
                self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()
            
    def on_checkEnableContourColorbar_toggled(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active()
        if widget.get_active():
            self.fig.clear()
            self.a = self.fig.add_subplot(111)
            if self.checkEnableContourFill.get_active():
                self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
                if self.checkEnableContourFillColorbar.get_active():
                    self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)
            self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
            self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
            if self.checkEnableContourLabels.get_active():
                self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
        else:
            a = self.fig.get_axes()
            if len(a) == 2:
                self.fig.delaxes(a[1])
            elif len(a) == 3:
                self.fig.delaxes(a[2])
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()
        
    def on_checkEnableContourFill_toggled(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active()
        if widget.get_active():
            self.fig.clear()
            self.a = self.fig.add_subplot(111)
            self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
            if self.checkEnableContourFillColorbar.get_active():
                self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)
            if self.checkEnableContourLines.get_active():
                self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
                if self.checkEnableContourLabels.get_active():
                    self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
                if self.checkEnableContourColorbar.get_active():
                    self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
            self.checkEnableContourFillColorbar.set_sensitive(True)
            self.lstContourFillColorMap.set_sensitive(True)
        else:
            self.a.clear()
            a = self.fig.get_axes()
            if len(a) == 2:
                self.fig.delaxes(a[1])
            elif len(a) == 3:
                self.fig.delaxes(a[1])
                self.fig.delaxes(a[2])
            self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
            if self.checkEnableContourLabels.get_active():
                self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
            if self.checkEnableContourColorbar.get_active():
                self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
            self.checkEnableContourLines.set_active(True)
            self.checkEnableContourFillColorbar.set_sensitive(False)
            self.lstContourFillColorMap.set_sensitive(False)
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()
        
    def on_checkEnableContourFillColorbar_toggled(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active()
        if widget.get_active():
            self.fig.clear()
            self.a = self.fig.add_subplot(111)
            self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
            self.colorbarContourFill = self.fig.colorbar(self.im, orientation='vertical', shrink=0.8)
            if self.checkEnableContourLines.get_active():
                self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
                if self.checkEnableContourLabels.get_active():
                    self.a.clabel(self.countourSet2D, inline=1, fontsize=10, colors='k')
                if self.checkEnableContourColorbar.get_active():
                    self.colorbarContour = self.fig.colorbar(self.countourSet2D, orientation='horizontal', shrink=0.8)
        else:
            a = self.fig.get_axes()
            if len(a) == 2 or len(a) == 3 :
                self.fig.delaxes(a[1])
        self.a.set_title(self.txtTitleLabel2D.get_text())
        self.fig.canvas.draw()

    def on_lstContourFillColorMap_changed(self, widget):
        model = self.lstContourFillColorMap.get_model()
        selected = self.lstContourFillColorMap.get_active()
        self.im = self.a.imshow(self.v1, interpolation='bilinear', origin='lower', extent=(-3,3,-2,2), cmap=model[selected][0])
        self.colorbarContourFill.update_bruteforce(self.im)#update_normal()
        self.countourSet2D = self.a.contour(self.v1, self.levels, origin='lower',linewidths=2,extent=(-3,3,-2,2),cmap=cm.get_cmap(name=model[selected][0]))
        if self.colorbarContour != None:
            self.colorbarContour.update_bruteforce(self.countourSet2D)
        self.fig.canvas.draw()
        
if __name__ == '__main__':
    objGUI = GUI()
    objGUI.loadVariables()
    objGUI.loadNumberNodes()
    #objGUI.initCustomizationParams()
    gtk.main()