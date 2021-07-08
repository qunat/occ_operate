
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file


display, start_display, add_menu, add_function_to_menu = init_display()
# loads  and displays a step file
the_shape = read_step_file('SFU01610-4.step')

from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_LinearProperties,BRepGProp_EdgeTool,BRepGProp_EdgeTool_Value
def line_clicked(shp, *kwargs):
    """ This function is called whenever a line is selected
    """
    for shape in shp:  # this should be a TopoDS_Edge
        print("Edge selected: ", shape)
        e = topods_Edge(shape)

        props = GProp_GProps()
        brepgprop_LinearProperties(e, props)

        length = props.Mass()
        print("此边的长度为: %f" % length)
        centerMass = props.CentreOfMass()
        print("此边的中心点为", centerMass.X(), centerMass.Y(), centerMass.Z())


display.DisplayShape(the_shape, update=True)
display.SetSelectionModeEdge()  # switch to edge selection mode
display.register_select_callback(line_clicked)


start_display()
