from PySide6.QtWidgets import QApplication, QMainWindow
from UI.BeginningScreen.widgets.path_choosing_widget import PathChoosingWidget
from UI.ProjectControlScreen.project_control_widget import ProjectControlWidget
from UI.ProjectControlScreen.preprocess_dialog.preprocess_dialog import PreprocessDialog
from UI.View.state_view_widget import StateViewWidget
from domain.statistics import Statistics
from pathlib import Path


def make_path_choosing_widget():
    w = PathChoosingWidget('input project path please',
                           default_feedback='haha feedback')
    w.Continue_Signal.connect(
        lambda s: print(f'continue please with such input {s}'))
    w.Return_Signal.connect(lambda: print('return immediately'))
    w.Something_Inputted_As_Path.connect(lambda s: print(f'the input was: {s}'))
    return w


def make_project_control_widget():
    w = ProjectControlWidget()
    w.Start_Preprocessing_Signal.connect(
        lambda: print('start preprocessing')
    )
    w.Open_Main_App_Signal.connect(
        lambda: print('open descriptor')
    )
    w.Export_Signal.connect(
        lambda: print('export')
    )

    d = PreprocessDialog()
    d.add_output_text('some text')
    d.add_output_text('another line')
    w.Start_Preprocessing_Signal.connect(
        lambda: d.exec()
    )

    w.statistics_widget.set_statistics(Statistics(
        Path('path here'),
        4,
        3,
        2,
        1,
        5,
        6,
        233,
    ))

    return w


class TempView:
    def __init__(self):
        self.q_app = QApplication()

        self.window = QMainWindow()
        self.window.setWindowTitle("App for development needs")
        self.window.setMinimumSize(800, 600)

        w = make_project_control_widget()

        self.window.setCentralWidget(w)
        pass

    def run(self):
        self.window.show()
        return_code = self.q_app.exec()
        return return_code


if __name__ == '__main__':
    TempView().run()

