from  PyQt5.QtWidgets  import *

from  matplotlib.backends.backend_qt5agg  import  FigureCanvas

from  matplotlib.figure  import  Figure

import  numpy  as  np
import  random

class  MplWidget ( QWidget ):

    def  __init__ ( self , parent  ):
        # super(MplWidget , self ).__init__(parent)
        QWidget . __init__ ( self ,  parent )

        self . canvas  =  FigureCanvas ( Figure ())

        vertical_layout  =  QVBoxLayout ()
        vertical_layout . addWidget ( self . canvas )

        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 )
        self . setLayout ( vertical_layout )

    def  update_graph ( self ):
    
        n_data = 50
        xdata = list(range(n_data))
        ydata = [random.randint(0, 10) for i in range(n_data)]

        self . canvas . axes . clear ()
        self . canvas . axes . plot (xdata, ydata, 'r' )
        self . canvas . draw ()
