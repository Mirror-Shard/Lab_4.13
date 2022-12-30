from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from EditorController import EditorController
from EditorModel import EditorModel

class GraphicsScene(QGraphicsScene):
    clicked = pyqtSignal(QPointF)
    released = pyqtSignal(QPointF)
    move = pyqtSignal(QPointF)

    def mousePressEvent(self, event):
        """
        Событие нажатия мышки
        """
        sp = event.scenePos()
        self.clicked.emit(sp)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Событие при разжатии мыши
        """
        sp = event.scenePos()
        self.released.emit(sp)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        Событие передвижения нажатой кнопки мыши
        """
        sp = event.scenePos()
        self.move.emit(sp)
        super().mouseMoveEvent(event)


class View(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = ""
        # Определение размеров и title окна GraphObject
        self.resize(550, 550)
        # self.setWindowTitle('')
        # Виджет для отображение GraphicsScene()
        self.grview = QGraphicsView()
        self.grview.scale(1, -1)
        # Фрейм на котором происходит отрисовка
        self.scene = GraphicsScene()
        self.scene.setSceneRect(-250, -250, 500, 500)
        # Включаем поддержку отслеживания нажатия/движения мыши
        self.setMouseTracking(True)
        # Подключаем GraphicsScene к QGraphicsView
        self.grview.setScene(self.scene)
        # Подключаем actions к сцене
        self.set_actions()
        # Подключаем дополнительные виджеты
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.grview)

        self.pen_color = Qt.black
        self.brush_color = Qt.black
        self.value_width = 1
        self.x1 = -250
        self.y1 = -250
        self.x2 = 500
        self.y2 = 500
        self.controller = EditorController(EditorModel(), self.x1, self.y1, self.x2, self.y2, self.scene)

        self.scene.clicked.connect(self.point1)
        self.scene.released.connect(self.point2)
        self.scene.move.connect(self.point3)

        self.trash_action.triggered.connect(self.clear)
        self.line_action.triggered.connect(self.click_line)
        self.rect_action.triggered.connect(self.click_rect)
        self.select_action.triggered.connect(self.click_select)
        self.circle_action.triggered.connect(self.click_circle)
        self.color_selection.triggered.connect(self.open_color_dialog)
        self.circuit_selection.triggered.connect(self.open_color_brush)
        self.fon_selection.triggered.connect(self.open_color_fon_dialog)
        self.spin_box.valueChanged.connect(self.spinbox_changed)

        self.show()

    def set_actions(self):
        self.figure_toolbar = QToolBar("figure")
        self.figure_toolbar.setIconSize(QSize(14, 14))
        self.basicToolBar = self.addToolBar(self.figure_toolbar)
        
        self.line_action = QAction(QIcon("images/line.png"), 'line', self)
        self.line_action.setStatusTip("line")
        self.figure_toolbar.addAction(self.line_action)
        
        self.rect_action = QAction(QIcon("images/rect.png"), 'rectangle', self)
        self.rect_action.setStatusTip("rect")
        self.figure_toolbar.addAction(self.rect_action)
        
        self.circle_action = QAction(QIcon("images/circle.ico"), 'circle', self)
        self.circle_action.setStatusTip("circle")
        self.figure_toolbar.addAction(self.circle_action)
        
        self.select_action = QAction(QIcon("images/select.ico"), 'select', self)
        self.select_action.setStatusTip("select")
        
        self.trash_action = QAction(QIcon("images/trash.png"), 'trash', self)
        self.trash_action.setStatusTip("trash")
        self.figure_toolbar.addAction(self.trash_action)
        
        self.color_selection = QAction('Сменить цвет \nфигуры', self)
        self.color_selection.setStatusTip("color")
        self.figure_toolbar.addAction(self.color_selection)
        
        self.circuit_selection = QAction('Сменить цвет \nконтура', self)
        self.circuit_selection.setStatusTip("color")
        self.figure_toolbar.addAction(self.circuit_selection)

        self.fon_selection = QAction('Сменить цвет \nфона', self)
        self.fon_selection.setStatusTip("color")
        self.figure_toolbar.addAction(self.fon_selection)
        self.label = QLabel(self)

        self.label.setText("Толщина ручки: ")
        self.figure_toolbar.addWidget(self.label)
        
        self.spin_box = QSpinBox(self)
        self.figure_toolbar.addWidget(self.spin_box)


    def clear(self):
        self.controller.clear()

    def open_color_dialog(self):
        brush_color = QColorDialog.getColor()
        self.controller.set_brush_prop(brush_color)

    def open_color_fon_dialog(self):
        fon_color = QColorDialog.getColor()
        self.scene.setBackgroundBrush(fon_color)

    def open_color_brush(self):
        self.pen_color = QColorDialog.getColor()
        self.controller.set_pen_props(self.pen_color, self.value_width)

    def spinbox_changed(self, value):
        self.value_width = value
        self.controller.set_pen_props(self.pen_color, self.value_width)

    def click_line(self):
        self.controller.set_object_type("line")
        self.controller.change_state("create")

    def click_rect(self):
        self.controller.set_object_type("rect")
        self.controller.change_state("create")

    def click_circle(self):
        self.controller.set_object_type("ellipse")
        self.controller.change_state("create")

    def click_select(self):
        self.controller.set_object_type("select")
        self.controller.change_state("empty")

    def point1(self, p):
        self.x1 = p.x()
        self.y1 = p.y()
        self.controller.mouse_clicked(self.x1, self.y1)

    def point2(self, p):
        self.x2 = p.x()
        self.y2 = p.y()
        self.controller.mouse_realised(self.x2, self.y2)

    def point3(self, p):
        self.x3 = p.x()
        self.y3 = p.y()
        self.controller.mouse_move(self.x3, self.y3)


def main():
    app = QtWidgets.QApplication(sys.argv)
    g = View()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
