import sys
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QComboBox
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon
import easygui
from templete_dealer import get_ids
from md2htmlconverter import convert_file


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_layout = QGridLayout()

        self.add_template_layout()
        self.template_group = QGroupBox("template")
        self.template_group.setLayout(self.template_layout)

        self.add_path_layout()
        self.path_group = QGroupBox("path")
        self.path_group.setLayout(self.path_layout)

        self.add_convert_layout()
        self.convert_group = QGroupBox("convert")
        self.convert_group.setLayout(self.convert_layout)

        self.main_layout.addWidget(self.template_group, 0, 0)
        self.main_layout.addWidget(self.path_group, 1, 0)
        self.main_layout.addWidget(self.convert_group, 2, 0)
        self.setLayout(self.main_layout)

    def add_template_layout(self):
        self.add_header_template_layout()
        self.add_navbar_template_layout()

        self.template_layout = QVBoxLayout()
        self.template_layout.addLayout(self.header_template_layout)
        self.template_layout.addLayout(self.navbar_template_layout)

    def add_header_template_layout(self):
        self.header_template_input_label = QLabel("header template")
        # add input text line
        self.header_template_input_text = QLineEdit(
            "https://zheminggu.github.io/myheadertemplete.html")
        self.header_template_input_text.returnPressed.connect(
            self.on_header_template_entered)
        # add combo box
        # change into dropdown in the future
        self.header_template_input_combo = QComboBox()
        self.header_template_input_combo.addItem("Input Your template")
        self.header_template_input_combo.currentTextChanged.connect(self.on_header_template_combo_changed)

        self.header_template_layout = QGridLayout()
        self.header_template_layout.addWidget(self.header_template_input_label, 0, 0)
        self.header_template_layout.addWidget(self.header_template_input_text, 1, 0, 1, 4)
        self.header_template_layout.addWidget(self.header_template_input_combo, 1, 5)

    def add_navbar_template_layout(self):
        self.navbar_template_input_label = QLabel("navbar template")
        # add user input text line
        self.navbar_template_input_text = QLineEdit(
            "https://zheminggu.github.io/myblognavbartemplete.html")
        self.navbar_template_input_text.returnPressed.connect(
            self.on_navbar_template_entered)
        # add combo box
        # change into dropdown in the future
        self.navbar_template_input_combo = QComboBox()
        self.navbar_template_input_combo.addItem("Pear")
        self.navbar_template_input_combo.addItem("Apple")
        self.navbar_template_input_combo.addItem("Banana")
        self.navbar_template_input_combo.currentTextChanged.connect(self.on_navbar_template_combo_changed)

        self.navbar_template_layout = QGridLayout()
        self.navbar_template_layout.addWidget(self.navbar_template_input_label, 0, 0)
        self.navbar_template_layout.addWidget(self.navbar_template_input_text, 1, 0, 1, 4)
        self.navbar_template_layout.addWidget(self.navbar_template_input_combo, 1, 5)

    def add_path_layout(self):
        self.add_input_file_layout()
        self.add_output_file_layout()
        self.path_layout = QVBoxLayout()
        self.path_layout.addLayout(self.input_file_layout)
        self.path_layout.addLayout(self.output_file_layout)

    def add_input_file_layout(self):
        self.input_button = QPushButton("Input")
        self.input_button.clicked.connect(self.on_input_button_clicked)
        self.input_file_path = QLineEdit("choose input file path")
        self.input_file_layout = QGridLayout()
        self.input_file_layout.addWidget(self.input_button, 0, 0)
        self.input_file_layout.addWidget(self.input_file_path, 0, 1, 0, 5)

    def add_output_file_layout(self):
        self.output_button = QPushButton("Output")
        self.output_button.clicked.connect(self.on_output_button_clicked)
        self.output_path = QLineEdit("choose output path")
        self.output_file_layout = QGridLayout()
        self.output_file_layout.addWidget(self.output_button, 0, 0)
        self.output_file_layout.addWidget(self.output_path, 0, 1, 0, 5)

    def add_convert_layout(self):
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.on_convert_button_clicked)
        self.convert_layout = QHBoxLayout()
        self.convert_layout.addWidget(self.convert_button)

    @Slot()
    def on_input_button_clicked(self):
        temp_string = easygui.fileopenbox()
        self.input_file_path.setText(temp_string)

    @Slot()
    def on_output_button_clicked(self):
        temp_string = easygui.diropenbox()
        self.output_path.setText(temp_string)

    @Slot()
    def on_header_template_entered(self):
        print(
            f"header template entered: {self.header_template_input_text.text()}")
        ids = get_ids(self.header_template_input_text.text())
        self.header_template_input_combo.clear()
        for i in ids:
            self.header_template_input_combo.addItem(i)

    @Slot()
    def on_navbar_template_entered(self):
        print(f"navbar template entered: {self.navbar_template_input_text.text()}")
        ids = get_ids(self.navbar_template_input_text.text())
        self.navbar_template_input_combo.clear()
        for i in ids:
            self.navbar_template_input_combo.addItem(i)

    @Slot()
    def on_header_template_combo_changed(self):
        print( f"current active header is : {self.header_template_input_combo.currentText()}")

    @Slot()
    def on_navbar_template_combo_changed(self):
        print(f"current active navbar is : {self.navbar_template_input_combo.currentText()}")

    @Slot()
    def on_convert_button_clicked(self):
        convert_file(
            self.get_input_path(),
            self.get_output_path(),
            self.header_template_input_text.text(),
            self.header_template_input_combo.currentText(),
            self.navbar_template_input_text.text(),
            self.navbar_template_input_combo.currentText())

    def get_input_path(self):
        return self.input_file_path.text().replace("\\", "\\\\")

    def get_output_path(self):
        return self.output_path.text().replace("\\", "\\\\")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = MyWidget()
    widget.setWindowTitle("zheminggu md2html converter")
    # widget.resize(800, 600)
    widget.setFixedWidth(600)
    widget.show()
    sys.exit(app.exec_())
