from ics import Calendar, Event

def ics_file_generator(json):
    calendario = Calendar()
    for evento in json:
        test = Event()
        test.name = evento['name'] 
        test.begin = evento['date'][:10]
        test.make_all_day()
        calendario.events.add(test)
    
    return str(calendario).encode("utf-8")