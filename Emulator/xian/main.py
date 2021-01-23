from  PyQt5.QtWidgets  import *
from  PyQt5.uic  import  loadUi

from  matplotlib.backends.backend_qt5agg  import  ( NavigationToolbar2QT  as  NavigationToolbar )

import  numpy  as  np

class  MatplotlibWidget ( QMainWindow ):

    def  __init__ ( self ):

        QMainWindow . __init__ ( self )

        loadUi ( "v4.ui" , self )

        self . GraphButton1 . clicked . connect ( self . MplWidget1 . update_graph )
        self . GraphButton2 . clicked . connect ( self . MplWidget2 . update_graph )
        self . GraphButton3 . clicked . connect ( self . MplWidget3 . update_graph )
        self . GraphButton4 . clicked . connect ( self . MplWidget4 . update_graph )

        self . addToolBar ( NavigationToolbar ( self . MplWidget1 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget2 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget3 . canvas ,  self ))
        self . addToolBar ( NavigationToolbar ( self . MplWidget4 . canvas ,  self ))

app  =  QApplication ([])
window  =  MatplotlibWidget ()
window . show ()
app . exec_ ()
