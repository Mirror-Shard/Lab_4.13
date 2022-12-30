from PyQt5 import QtGui
from PyQt5.QtGui import *
from Frame import Frame
from Painter import Painter
from Figures import Line, Rectangle, Ellipse
from Properties import Properties, PenProps, BrushProps, BackgroundBrush
from Painter import Painter

class EditorModel:
    def __init__(self):
        self.painter = Painter()
        self.store = Store()
        self.selection_store = SelectionStore()
        self.object_factory = ObjectFactory(self.store)
        self.scene = Scene(self.store, self.painter, self.selection_store)
        self.object_state = False
        self.move_state = False
        self.curr_object = None
        self.last_object = False

    def try_select(self, x, y):
        self.object_state = False
        for object in self.store.list:
            if object.in_body(x, y):
                self.selection_store.list.append(object.create_selection())
                object.select = True
                self.scene.repaint()
                return True
        return False

    def try_grab(self, x, y):
        return self.selection_store.try_grab(x, y)

    def try_drag_to(self, x, y):
        self.selection_store.try_drag_to(x, y)
        if self.selection_store.drag_state:
            self.scene.repaint()

    def clear_selection(self):
        self.selection_store.list = []
        self.curr_object = None
        for object in self.store.list:
            object.select = False
        self.scene.repaint()

    def set_port(self, x1, y1, x2, y2, painter):
        self.painter.set_port(x1, y1, x2, y2, painter)

    def create_object(self, x, y):
        self.object_factory.create_object(x, y)
        self.selection_store.list.append(self.store.list[len(self.store.list) - 1].create_selection())
        self.scene.repaint()

    def set_pen_props(self, pen_color, pen_width):
        self.object_factory.set_pen_props(pen_color, pen_width)

    def set_brush_prop(self, brush_prop):
        self.object_factory.set_brush_prop(brush_prop)

    def set_fon_prop(self, fon_color):
        self.object_factory.set_fon_prop(fon_color)

    def set_object_type(self, object):
        self.object_factory.set_object_type(object)

    def clear(self):
        self.store.clear()
        self.selection_store.list = []
        self.scene.repaint()

    def repaint(self):
        self.scene.repaint()

class ObjectFactory:
    def __init__(self, store):
        self.object_type = None
        self.pen_props = PenProps(QtGui.QColor("green"), 1)
        self.brush_prop = BrushProps(QtGui.QColor("green"))
        self.fon_color = BackgroundBrush(QtGui.QColor("white"))
        self.store = store

    def set_pen_props(self, pen_color, pen_width):
        self.pen_props = PenProps(pen_color, pen_width)

    def set_fon_prop(self, fon_color):
        self.fon_color = BackgroundBrush(fon_color)

    def set_brush_prop(self, brush_prop):
        self.brush_prop = BrushProps(brush_prop)

    def set_object_type(self, object):
        self.object_type = object

    def create_object(self, x, y):
        frame = Frame(x, y, x, y)
        prop = Properties()
        prop.prop_group.list_prop.append(self.pen_props)
        prop.prop_group.list_prop.append(self.brush_prop)

        if self.object_type == "rect":
            rect = Rectangle(frame, prop)
            self.store.add(rect)

        elif self.object_type == "ellipse":
            ellipse = Ellipse(frame, prop)
            self.store.add(ellipse)

        elif self.object_type == "line":
            line = Line(frame, prop)
            self.store.add(line)


class Store:
    def __init__(self):
        self.list = []

    def add(self, object):
        self.list.append(object)

    def clear(self):
        self.list = []


class SelectionStore:

    def __init__(self):
        self.list = []

    def clear_selection(self):
        self.list = []

    def try_grab(self, x, y):
        self.grabbed = False
        for select in self.list:
            if select.try_grab(x, y):
                self.grabbed = True
        return self.grabbed

    def try_drag_to(self, x, y):
        self.drag_state = False
        for select in self.list:
            select.try_drag_to(x, y)
            self.drag_state = True
        self.list[0].set_point(x, y)


class Scene:
    def __init__(self, store, painter, selection_store):
        self.store = store
        self.painter = painter
        self.selection_store = selection_store

    def repaint(self):
        self.painter.clear()
        for object in self.store.list:
            object.draw(self.painter)
        for select in self.selection_store.list:
            select.draw(self.painter)
