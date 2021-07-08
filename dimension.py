
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_AngleDimension



display, start_display, add_menu, add_function_to_menu = init_display()
# loads  and displays a step file
the_shape = read_step_file('SFU01610-4.step')
context = display.Context



def get_boundingbox(shape, tol=1e-6, use_mesh=True):
    """ return the bounding box of the TopoDS_Shape `shape`
    Parameters
    ----------
    shape : TopoDS_Shape or a subclass such as TopoDS_Face
        the shape to compute the bounding box from
    tol: float
        tolerance of the computed boundingbox
    use_mesh : bool
        a flag that tells whether or not the shape has first to be meshed before the bbox
        computation. This produces more accurate results
    """
    bbox = Bnd_Box()
    bbox.SetGap(tol)
    if use_mesh:
        mesh = BRepMesh_IncrementalMesh()
        mesh.SetParallelDefault(True)
        mesh.SetShape(shape)
        mesh.Perform()
        assert mesh.IsDone()
    brepbndlib_Add(shape, bbox, use_mesh)

    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return xmin, ymin, zmin, xmax, ymax, zmax, xmax-xmin, ymax-ymin, zmax-zmin

num=0
ais_shape=AIS_ColoredShape(the_shape)
for e in TopologyExplorer(the_shape).shells():
        rnd_color = (random(), random(), random())
        display.DisplayColoredShape(e,color=rgb_color(random(), random(), random()),update=True)
        display.FitAll()
        #display.View_Rear()
        path='./'+str(num)+".bmp"
        display.View.Dump(path)
        num+=1
        display.EraseAll()
        ais_shape.SetCustomColor(e, rgb_color(random(), random(), random()))
        volume=get_boundingbox(e)
        print("长: %f,宽: %f,高: %f" % (volume[6],volume[7],volume[8]))
        
        
        
        
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_LinearProperties,BRepGProp_EdgeTool,BRepGProp_EdgeTool_Value
list_edge=[]
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
        list_edge.append(e)
        if len(list_edge)==2:
            pass
            am = AIS_AngleDimension(list_edge[0], list_edge[1])
            print(123)
            display.Context.Display(am, True)
            list_edge.clear()





context.Display(ais_shape,True)
context.SetTransparency(ais_shape, 0, True)
owner = ais_shape.GetOwner()
#drawer = ais_shape.DynamicHilightAttributes()
# TODO: how do we set the color ? Quantity_NOC_RED
#context.HilightWithColor(ais_shape, drawer, True)
display.SetSelectionModeEdge() # switch to edge selection mode
#display.SetModeShaded()
display.register_select_callback(line_clicked)


start_display()
