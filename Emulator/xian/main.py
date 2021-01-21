from  PyQt5.QtWidgets  import *
from  PyQt5.uic  import  loadUi

from  matplotlib.backends.backend_qt5agg  import  ( NavigationToolbar2QT  as  NavigationToolbar )

import  numpy  as  np
import  random

class  MatplotlibWidget ( QMainWindow ):

    def  __init__ ( self ):

        QMainWindow . __init__ ( self )

        loadUi ( "v4.ui" , self )

        self . setWindowTitle ( "Plot Graph" )

        self . generate1 . clicked . connect ( self . update_graph1 )
        self . generate2 . clicked . connect ( self . update_graph2 )
        self . generate3 . clicked . connect ( self . update_graph3 )
        self . generate4 . clicked . connect ( self . update_graph4 )

        self . addToolBar ( NavigationToolbar ( self . MplWidget1 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget2 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget3 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget4 . canvas ,  self ))


    def  update_graph1 ( self ):

        n_data = 50
        xdata = list(range(n_data))
        ydata = [random.randint(0, 10) for i in range(n_data)]

        self . MplWidget1 . canvas . axes . clear ()
        self . MplWidget1 . canvas . axes . plot (xdata, ydata, 'r' )
        self . MplWidget1 . canvas . draw ()

    def  update_graph2 ( self ):

        n_data = 50
        xdata = list(range(n_data))
        ydata = [random.randint(0, 10) for i in range(n_data)]

        self . MplWidget2 . canvas . axes . clear ()
        self . MplWidget2 . canvas . axes . plot (xdata, ydata, 'r' )
        self . MplWidget2 . canvas . draw ()

    def  update_graph3 ( self ):

        n_data = 50
        xdata = list(range(n_data))
        ydata = [random.randint(0, 10) for i in range(n_data)]

        self . MplWidget3 . canvas . axes . clear ()
        self . MplWidget3 . canvas . axes . plot (xdata, ydata, 'r' )
        self . MplWidget3 . canvas . draw ()

    def  update_graph4 ( self ):

        n_data = 50
        xdata = list(range(n_data))
        ydata = [random.randint(0, 10) for i in range(n_data)]

        self . MplWidget4 . canvas . axes . clear ()
        self . MplWidget4 . canvas . axes . plot (xdata, ydata, 'r' )
        self . MplWidget4 . canvas . draw ()


app  =  QApplication ([])
window  =  MatplotlibWidget ()
window . show ()
app . exec_ ()
