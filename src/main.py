import time
import os
import csv

class Stopwatch:
    """A simple Class that controls a stopwatch interface."""

    def __init__(self, start_time = -1, end_time = -1, read_only = False):
        self.start_time = start_time
        self.end_time = end_time
        self.is_stopwatch_on = False
        self.read_only = read_only
    
    def start_stopwatch(self):
        if(self.read_only == False):
            self.start_time = time.time()
            self.end_time = -1
            self.is_stopwatch_on = True
        else:
            raise StopwatchReadOnly("stopwatch is set to read only")

    def end_stopwatch(self):
        if(self.read_only == True):
            raise StopwatchReadOnly("stopwatch is set to read only")
        elif(self.is_stopwatch_on == True):
            self.end_time = time.time()
            self.is_stopwatch_on = False
        else:
            raise StopwatchNotOn("stopwatch not on")

    def get_time_elapsed(self):
        if(self.start_time > -1):
            if(self.is_stopwatch_on == True):
                return time.time() - start_time
            else:
                return self.end_time - self.start_time
        else:
            raise StopwatchNotStarted("stopwatch not started")

class StopwatchNotOn(Exception):
    pass

class StopwatchNotStarted(Exception):
    pass

class StopwatchReadOnly(Exception):
    pass

class CSVManager:
    """Class which manages the reading and righting of CSV project files."""
    
    def __init__(self, default_path = './projects'):
        os.makedirs(default_path, exist_ok=True)
        self.default_path = default_path
        
    def write_stopwatch(self, file_name, stopwatch):
        # New file
        if not os.path.exists(self.default_path + file_name):
            with open(self.default_path + file_name, 'w', newline='') as csvfile:
                stopwatch_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                stopwatch_writer.writerow([stopwatch.start_time, stopwatch.end_time, stopwatch.get_time_elapsed()])
                
        # Is a file
        elif os.path.isfile(self.default_path + file_name):
            # Is compatible
            with open(self.default_path + file_name, 'a', newline='') as csvfile:
                stopwatch_writer = csv.writer(csvfile, delimiter=',',
                                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
                stopwatch_writer.writerow([stopwatch.start_time, stopwatch.end_time, stopwatch.get_time_elapsed()])
            # Is not compatible
        else:
            # Is a dir
            raise FileNotFound("file not found")

    def read_csv(self, file_name):
        stopwatch_list = []
        if os.path.isfile(self.default_path + '/' + file_name):
            if True:#Compatible
                with open(self.default_path + '/' + file_name, 'r') as f:
                    csv_reader = csv.reader(f, delimiter=',', quotechar='|')
                    for row in csv_reader:
                        stopwatch = Stopwatch()
                        stopwatch.start_time = int(row[0])
                        stopwatch.end_time = int(row[1])
                        stopwatch_list.append(stopwatch)
            else: #Incompatible
                raise FileNotFound("file not found")
        else:
            raise FileNotFound("file not found")

        return stopwatch_list
        
class FileNotFound(Exception):
    pass

class FileNotCompatible(Exception):
    pass

