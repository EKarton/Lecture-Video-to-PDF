class SubtitlePart:
    """A class that represents a part of the entire video's subtitle

    Attributes
    ----------
    start_time : int
        The starting time of this subtitle's part in milliseconds
    end_time : int
        The end time of this subtitle's part in milliseconds
    text : str
        The text corresponding to the subtitle's part
    """

    def __init__(self, start_time, end_time, text):
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self):
        return "{}-{}".format(self.start_time, self.end_time)

    def __repr__(self):
        return self.__str__()
