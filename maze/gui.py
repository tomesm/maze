from PyQt5 import QtWidgets, uic, QtGui, QtCore, QtSvg
import numpy
import maze
import os

ROWS = 15
COLUMNS = 15

def get_filename(name):
    return os.path.join(os.path.dirname(__file__), name)

CELL_SIZE = 32

SVG_GRASS = QtSvg.QSvgRenderer(get_filename('img/grass.svg'))
SVG_WALL = QtSvg.QSvgRenderer(get_filename('img/wall.svg'))

VALUE_ROLE = QtCore.Qt.UserRole

def pixels_to_logical(x, y):
    return y // CELL_SIZE, x // CELL_SIZE


def logical_to_pixels(row, column):
    return column * CELL_SIZE, row * CELL_SIZE


class GridWidget(QtWidgets.QWidget):

    def __init__(self, array):
        super().__init__()
        self.array = array
        size = logical_to_pixels(*array.shape)
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.resize(*size)

    def paintEvent(self, event):
        rect = event.rect()

        painter = QtGui.QPainter(self) # self aby nam kreslil na to okynko

        # minimalni souradnice
        row_min, col_min = pixels_to_logical(rect.left(), rect.top())

        row_min = max(row_min, 0) # kdyz dostanu zaporny index od OS k prekresleni, musi mzacit od nuly
        col_min = max(col_min, 0)
        # maximalni souradnice
        row_max, col_max = pixels_to_logical(rect.right(), rect.bottom())

        row_max = min(row_max + 1, self.array.shape[0])
        col_max = min(col_max + 1, self.array.shape[1])
        # ted vime kde zacit a kde skoncit

        for row in range(row_min, row_max):
            for column in range(col_min, col_max):
                # get rectangle to paint
                x, y = logical_to_pixels(row, column)
                rect = QtCore.QRectF(x, y, CELL_SIZE, CELL_SIZE)

                # bila pro polopruhledne obrazky
                color = QtGui.QColor(255, 255, 255)
                painter.fillRect(rect, QtGui.QBrush(color))
                # dame travu vsude, resp. zed na travu
                SVG_GRASS.render(painter, rect)
                # zdi tam, kde patri
                if self.array[row, column] < 0:
                    SVG_WALL.render(painter, rect)


    def mousePressEvent(self, event):
        row, column = pixels_to_logical(event.x(), event.y())
        rows, columns = self.array.shape
        # je to, kam jsem kliknul mezi nulou a koncem matice?
        # muzu totiz kliknout uplne vedle
        if 0 <= row < rows and 0 <= column < columns:
            if event.button() == QtCore.Qt.LeftButton:
                self.array[row, column] = self.selected
            elif event.button() == QtCore.Qt.RightButton:
                self.array[row, column] = 0
            else:
                return
            self.update()




def main():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()

    with open(get_filename('ui/MainWindow.ui')) as file:
        uic.loadUi(file, window)

    def new_dialog():
        dialog = QtWidgets.QDialog(window)

        with open(get_filename('ui/newmaze.ui')) as file:
            uic.loadUi(file, dialog)

        result = dialog.exec()

        if result == QtWidgets.QDialog.Rejected:
            return

        # vyberu si konkretni widget a zavolan value
        cols = dialog.findChild(QtWidgets.QSpinBox, 'spinWidth').value()
        rows = dialog.findChild(QtWidgets.QSpinBox, 'spinHeight').value()

        grid.array = maze.generator.generate_maze(cols, rows)
        # tohle v init tohoto gridu
        size = logical_to_pixels(*array.shape)
        grid.setMinimumSize(*size)
        grid.setMaximumSize(*size)
        grid.resize(*size)
        grid.update()


    action = window.findChild(QtWidgets.QAction, 'actionNew')
    action.triggered.connect(new_dialog)
    array = maze.generator.generate_maze(15,15)
    scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
    grid = GridWidget(array)
    scroll_area.setWidget(grid)

    palette = window.findChild(QtWidgets.QListWidget, 'listWidget')

    item = QtWidgets.QListWidgetItem('Grass')
    icon = QtGui.QIcon('img/grass.svg')
    item.setIcon(icon)
    item.setData(VALUE_ROLE, 0)
    palette.addItem(item)

    item = QtWidgets.QListWidgetItem('Wall')
    icon = QtGui.QIcon('img/wall.svg')
    item.setIcon(icon)
    item.setData(VALUE_ROLE, -1)
    palette.addItem(item)
    # TODO: writ function for adding items

    def item_activated():
        for item in palette.selectedItems():
            grid.selected = item.data(VALUE_ROLE)

    palette.itemSelectionChanged.connect(item_activated)
    # v gridu musi byt nejaka prednastavena hodnota na zacatku
    # prednastavime zed jako defaultni
    palette.setCurrentRow(1)

    window.show()
    return app.exec()

main()
