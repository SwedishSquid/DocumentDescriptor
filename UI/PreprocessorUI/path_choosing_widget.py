from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QLabel
from PySide6.QtCore import Signal
from UI.BeginningScreen.select_folder_location_widget \
    import SelectFolderLocationWidget


class PathChoosingWidget(QWidget):
    """
    to unblock continue button use enable_continue_button method
    Emitted signals:
    Continue_Signal - user pressed continue button;
    Return_Signal - user pressed return button
    """
    Continue_Signal = Signal(str)
    Return_Signal = Signal()
    Something_Inputted_As_Path = Signal(str)

    def __init__(self, input_description: str,
                 input_field_hint: str = 'write here',
                 return_button_text: str = 'Back',
                 continue_button_text: str = 'Continue',
                 default_feedback: str = ''):
        super(PathChoosingWidget, self).__init__()

        self.folder_selection_widget = SelectFolderLocationWidget(
            caption=input_description, input_field_info=input_field_hint)
        self.folder_selection_widget.Some_Input_Signal.connect(
            self._on_input_changed)

        self.feedback_label = QLabel(text=default_feedback)

        self.return_button = QPushButton(text=return_button_text)
        self.return_button.clicked.connect(
            lambda: self.Return_Signal.emit()
        )
        self.continue_button = QPushButton(text=continue_button_text)
        self.continue_button.clicked.connect(
            lambda: self.Continue_Signal.emit(self.get_input_text())
        )
        self.continue_button.setEnabled(False)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.return_button)
        buttons_layout.addWidget(self.continue_button)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(self.folder_selection_widget)
        main_layout.addWidget(self.feedback_label)
        main_layout.addLayout(buttons_layout)
        pass

    def get_input_text(self):
        return self.folder_selection_widget.get_input_text()

    def enable_continue_button(self):
        """every time user change there input, continue button disables
        use Something_Inputted_As_Path signal to check if input is correct
        and then unblock continue button with this function"""
        self.continue_button.setEnabled(True)
        pass

    def set_feedback_string(self, text: str):
        """feedback string = text shown to user after they typed in data;
        may help user understand the problem, if input is incorrect;
        automatically cleans up every time user input changes"""
        self.feedback_label.setText(text)
        pass

    def _disable_continue_button(self):
        """by default button is disabled;
        every time input changed - it is automatically disabled;
        so it seems no reasons exist to make this method public"""
        self.continue_button.setEnabled(False)
        pass

    def _on_input_changed(self, new_input_text):
        self._disable_continue_button()
        self.set_feedback_string('')
        self.Something_Inputted_As_Path.emit(new_input_text)
        pass
    pass
