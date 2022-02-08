import enum


class UserModelConstants(enum.Enum):
    """User model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    # Booleans.
    TRUE = True
    FALSE = False


class TeacherModelConstants(enum.Enum):
    """Teacher model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    CARD_ID_DEFAULT_NUMBER = 'UNI-0000000'

    # Booleans.
    TRUE = True
    FALSE = False


class StudentsModelConstants(enum.Enum):
    """Student model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    CARD_ID_DEFAULT_NUMBER = 'STU-0000000'

    # Booleans.
    TRUE = True
    FALSE = False
