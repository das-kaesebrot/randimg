class Constants:
    ALLOWED_DIMENSIONS = [2048, 1042, 512, 256, 128, 64, 32, 16]
    DEFAULT_FORMAT = "png"
    
    @staticmethod
    def get_default_width():
        return Constants.ALLOWED_DIMENSIONS[2]
    
    @staticmethod
    def get_max_width():
        return Constants.ALLOWED_DIMENSIONS[0]
    