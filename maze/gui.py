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



class MazeGui(object):
    """ Class representing maze GUI """
    def __init__(self):
        """ Init all neded stuff """
        self.app = QtWidgets.QApplication([]) # init app
        self.window = window = QtWidgets.QMainWindow() # set main GUI window
        self.array = maze.generator.generate_maze(COLUMNS,ROWS)
        self.new_dialog = None

        with open(get_filename('ui/MainWindow.ui')) as file:
            uic.loadUi(file, window)

        self.scroll_area = window.findChild(QtWidgets.QScrollArea, 'scrollArea')
        self.grid = grid = GridWidget(self.array)
        self.scroll_area.setWidget(grid)

        self.palette = window.findChild(QtWidgets.QListWidget, 'listWidget')

        item = QtWidgets.QListWidgetItem('Grass')
        icon = QtGui.QIcon(get_filename('img/grass.svg'))
        item.setIcon(icon)
        item.setData(VALUE_ROLE, 0)
        self.palette.addItem(item)

        item = QtWidgets.QListWidgetItem('Wall')
        icon = QtGui.QIcon(get_filename('img/wall.svg'))
        item.setIcon(icon)
        item.setData(VALUE_ROLE, -1)
        self.palette.addItem(item)
        # TODO: writ function for adding items

        self.palette.itemSelectionChanged.connect(self._item_activated)
        # v gridu musi byt nejaka prednastavena hodnota na zacatku
        # prednastavime zed jako defaultni
        self.palette.setCurrentRow(1)

        self._action('actionNew').triggered.connect(self._new_dialog)





    def _action(self, name):
        return self.window.findChild(QtWidgets.QAction, name)


    def _item_activated(self):
        for item in self.palette.selectedItems():
            self.grid.selected = item.data(VALUE_ROLE)

    def _new_dialog():
        self.new_dialog = dialog = QtWidgets.QDialog(self.window)
        dialog.setModal(True)

        with open(get_filename('ui/newmaze.ui')) as file:
            uic.loadUi(file, dialog)

        dialog.show()
        dialog.finished.connect(self._new_finished)


    def _new_finished(self, result):
        dialog = self.new_dialog
        self.new_dialog =  None

        if not result:
            dialog.destroy()
            return

        # vyberu si konkretni widget a zavolan value
        cols = dialog.findChild(QtWidgets.QSpinBox, 'spinWidth').value()
        rows = dialog.findChild(QtWidgets.QSpinBox, 'spinHeight').value()
        dialog.destroy()

        self.array = self.grid.array = maze.generator.generate_maze(cols, rows)
        # tohle v init tohoto gridu
        size = logical_to_pixels(*self.array.shape)
        self.grid.setMinimumSize(*size)
        self.grid.setMaximumSize(*size)
        self.grid.resize(*size)
        self.grid.update()


    def run(self):
        self.window.show()
        return self.app.exec_()


def main():
    gui = MazeGui()
    return gui.run()
