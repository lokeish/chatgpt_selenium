class CreateFolderFailure(Exception):
    "Raised when folder creation fails"
    pass

class FilesFilterFailure(Exception):
    """Raised when filtering files from source folder fails"""
    pass

class OcrFailure(Exception):
    """Raised when ocr fails"""
    pass

class TextCleaningFailure(Exception):
    """Raised when text cleaning fails"""
    pass