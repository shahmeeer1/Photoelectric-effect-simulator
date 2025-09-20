# analyse/__init__.py

# Expose main GUI class
from .analyse_gui import analyse_gui

# Expose Graph subclasses
from .ke_vs_f import KE_VS_F
from .i_vs_f import I_VS_F

# Expose utility classes
from .graph_base import Graph
from .regression import Regression
