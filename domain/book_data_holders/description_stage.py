import enum


class DescriptionStage(enum.IntEnum):
    NOT_STARTED = 0,
    IN_PROGRESS = 1,
    FINISHED = 2,
    REJECTED = 3,
