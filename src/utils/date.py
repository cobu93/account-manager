from datetime import datetime

def parse_file_date(d: str):    
    day = datetime.strptime(d, "%m/%d")
    day = day.replace(year=datetime.now().year)
    return day