from collections import defaultdict
import datetime

class EventHandler:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, function):
        if function not in self.subscribers[event_type]:
            self.subscribers[event_type].append(function)

    def post_event(self, event_type, data):
        if event_type in self.subscribers:
            for fn in self.subscribers[event_type]:
                fn((event_type,*data))
    
            # self.log((event_type,*data))

        else:
            self.subscribers[event_type] = []
            self.subscribe(event_type,self.log)
            self.log((event_type,*data))

    def log(self,data):
        event_type, *data = data
        if event_type != "Error":
            print(f"[EventLogger] {datetime.datetime.now()}__ Event:'{event_type}' data: {data}")
        else:
            print(f"[EventLogger] {datetime.datetime.now()}__ [!] Error: {data[0]}")


        
