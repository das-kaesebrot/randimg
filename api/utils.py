class Utils:
    def __init__(self):
        pass

    @staticmethod
    def clamp(val, low, high):
        return max(low, min(val, high))
