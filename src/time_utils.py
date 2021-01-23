def convert_clock_time_to_timestamp_ms(clock_time):
    """Converts time from HH:MM:SS format to timestamp format (in milliseconds)
    For instance, given "00:05:38", it will return 338000

    Parameters
    ----------
    clock_time : str
        The clock time in HH:mm:ss format

    Returns
    -------
    timestamp_ms : int
        Timestamp in milliseconds
    """
    clock_time_parts = clock_time.split(":")
    if len(clock_time_parts) != 3:
        raise Exception(
            "Illegal argument! Expected 3 parts, instead {} in {}".format(
                len(clock_time_parts), clock_time
            )
        )

    hours = int(clock_time_parts[0])
    minutes = int(clock_time_parts[1])
    seconds = float(clock_time_parts[2])

    return (hours * 3600000) + (minutes * 60000) + (seconds * 1000)


def convert_timestamp_ms_to_clock_time(timestamp_ms):
    """Converts time in milliseconds to clock time
    For instance, given 338000, it will return "00:05:38"

    Parameters
    ----------
    timestamp_ms : int
        Timestamp in milliseconds

    Returns
    -------
    clock_time : str
        The clock time in HH:mm:ss format
    """
    hours = int(timestamp_ms / 3600000)
    minute = int((timestamp_ms % 3600000) / 60000)
    seconds = float((timestamp_ms % 3600000 % 60000) / 1000)

    if int(seconds) == seconds:
        seconds = int(seconds)

    formatted_seconds = str(seconds)
    if seconds < 10:
        formatted_seconds = "0" + str(seconds)

    return str(hours).zfill(2) + ":" + str(minute).zfill(2) + ":" + formatted_seconds
