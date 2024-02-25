from domain.book_data_holders.description_stage import DescriptionStage
from PySide6.QtGui import QColorConstants, QColor

color_by_stage_for_widget_background = {
    DescriptionStage.NOT_STARTED: QColorConstants.Gray,
    DescriptionStage.IN_PROGRESS: QColor(211, 188, 0),
    DescriptionStage.REJECTED: QColor(218, 106, 95),
    DescriptionStage.FINISHED: QColor(76, 148, 0)
}

color_by_stage_for_text_document_background = {
    DescriptionStage.NOT_STARTED: QColorConstants.White,
    DescriptionStage.IN_PROGRESS: QColor(255, 238, 154),
    DescriptionStage.REJECTED: QColor(255, 195, 154),
    DescriptionStage.FINISHED: QColor(206, 255, 154)
}

