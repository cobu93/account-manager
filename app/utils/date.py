from datetime import datetime

def parse_file_date(d: str):   
    """
    Parsing string dates to datetime.

    The accepted formats are:
        - month/day
    """ 
    day = datetime.strptime(d, "%m/%d")
    day = day.replace(year=datetime.now().year)
    return day