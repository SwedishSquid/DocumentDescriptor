from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,\
    QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, Qt
from UI.BeginningScreen.widgets.select_folder_location_widget \
    import SelectFolderLocationWidget


class PathChoosingWidget(QWidget):
    """
    to unblock continue button use enable_continue_button method
    Emitted signals:
    Continue_Signal - user pressed continue button;
    Return_Signal - user pressed return button;
    Something_Inputted_As_Path - user changed input field;
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
        self.feedback_label.setFont(QFont('Arial', 12))
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.return_button = self._make_button(text=return_button_text)
        self.return_button.clicked.connect(
            lambda: self.Return_Signal.emit()
        )
        self.continue_button = self._make_button(text=continue_button_text)
        self.continue_button.clicked.connect(
            self._on_continue_clicked
        )
        self.continue_button.setEnabled(False)

        select_folder_and_feedback_layout = QVBoxLayout()
        select_folder_and_feedback_layout.addWidget(self.folder_selection_widget)
        select_folder_and_feedback_layout.addWidget(self.feedback_label)
        select_folder_and_feedback_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(3)
        buttons_layout.addWidget(self.return_button, 2)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.continue_button, 2)
        buttons_layout.addStretch(3)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        # main_layout.addStretch()
        main_layout.addLayout(select_folder_and_feedback_layout)
        main_layout.addLayout(buttons_layout)
        pass

    def get_input_text(self):
        return self.folder_selection_widget.get_input_text()

    def clear_input_text(self):
        self.folder_selection_widget.clear_input_text()

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

    def _on_continue_clicked(self):
        self.Continue_Signal.emit(self.get_input_text())
        pass

    def _make_button(self, text):
        button = QPushButton(text=text)
        font = QFont('Arial', 12)
        button.setFont(font)
        button.setFixedSize(270, 50)
        return button
    pass
