import sys
import vtk
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class STLVisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("3D STL Visualization Assignment")

        # Create a VTK render window and interactor
        self.ren_win = vtk.vtkRenderWindow()
        self.ren = vtk.vtkRenderer()
        self.ren_win.AddRenderer(self.ren)
        self.vtk_widget = QVTKRenderWindowInteractor(parent=self, rw=self.ren_win)

        # Create buttons
        self.load_btn = QPushButton("Load STL File", self)
        self.load_btn.clicked.connect(self.load_stl)
        self.unload_btn = QPushButton("Unload STL File", self)
        self.unload_btn.clicked.connect(self.unload_stl)
        self.unload_btn.setEnabled(False)

        # New buttons for translation
        self.translate_x_btn = QPushButton("Translate X", self)
        self.translate_x_btn.clicked.connect(lambda: self.translate_stl(1, 0, 0))
        self.translate_x_btn.setEnabled(False)

        self.translate_y_btn = QPushButton("Translate Y", self)
        self.translate_y_btn.clicked.connect(lambda: self.translate_stl(0, 1, 0))
        self.translate_y_btn.setEnabled(False)

        # Layout setup
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Horizontal layout for buttons on the right
        hbox = QHBoxLayout()
        hbox.addWidget(self.vtk_widget)

        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Adjust the spacing between buttons
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.unload_btn)
        button_layout.addWidget(self.translate_x_btn)
        button_layout.addWidget(self.translate_y_btn)

        hbox.addLayout(button_layout)
        layout.addLayout(hbox)

        # STL file variables
        self.stl_actor = None
        self.stl_reader = vtk.vtkSTLReader()
        self.stl_file_path = None

    def load_stl(self):
        # Open file dialog to select STL file
        file_dialog = QFileDialog(self, "Open STL File", "", "STL Files (*.stl)")
        if file_dialog.exec_():
            stl_file = file_dialog.selectedFiles()[0]
            self.visualize_stl(stl_file)
            self.stl_file_path = stl_file
            self.unload_btn.setEnabled(True)
            self.translate_x_btn.setEnabled(True)
            self.translate_y_btn.setEnabled(True)

    def visualize_stl(self, file_path):
        # Create a reader to read the STL file
        self.stl_reader.SetFileName(file_path)

        # Create a mapper and actor to display the STL file
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.stl_reader.GetOutputPort())
        self.stl_actor = vtk.vtkActor()
        self.stl_actor.SetMapper(mapper)

        # Clear the previous actor, if any
        self.ren.RemoveAllViewProps()

        # Add the new actor to the renderer and render
        self.ren.AddActor(self.stl_actor)
        self.ren.ResetCamera()
        self.ren_win.Render()

    def unload_stl(self):
        # Remove STL actor from renderer and render
        if self.stl_actor:
            self.ren.RemoveActor(self.stl_actor)
            self.ren_win.Render()

            # Clean up STL reader and disable the buttons
            self.stl_reader.SetFileName("")  # Clear the file name to prevent issues with reloading the same file
            self.stl_actor = None
            self.unload_btn.setEnabled(False)
            self.translate_x_btn.setEnabled(False)
            self.translate_y_btn.setEnabled(False)
            self.stl_file_path = None

    def translate_stl(self, dx, dy, dz):
        if self.stl_actor:
            transform = vtk.vtkTransform()
            transform.Translate(dx, dy, dz)
            self.stl_actor.SetUserTransform(transform)
            self.ren_win.Render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = STLVisualizationApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
