from datetime import datetime, timedelta
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

    def pretty_start_time(self):
        return datetime.utcfromtimestamp(int(self.start_time)).strftime('%Y-%m-%d %H:%M:%S')
        
    def end_stopwatch(self):
        if(self.read_only == True):
            raise StopwatchReadOnly("stopwatch is set to read only")
        elif(self.is_stopwatch_on == True):
            self.end_time = time.time()
            self.is_stopwatch_on = False
        else:
            raise StopwatchNotOn("stopwatch not on")

    def pretty_end_time(self):
        return datetime.utcfromtimestamp(int(self.end_time)).strftime('%Y-%m-%d %H:%M:%S')
        
    def get_time_elapsed(self):
        if(self.start_time > -1):
            if(self.is_stopwatch_on == True):
                return time.time() - start_time
            else:
                return self.end_time - self.start_time
        else:
            raise StopwatchNotStarted("stopwatch not started")

    def pretty_duration(self):
        return str(timedelta(0, int(self.get_time_elapsed())))

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
        self.have_set = False

    def set_dir(self):
        if(not self.have_set):
            self.have_set = True
            os.chdir(self.default_path)
            
    def write_stopwatch(self, file_name, stopwatch):
        self.set_dir()
        # New file
        if not os.path.exists(file_name):
            with open(file_name, 'w', newline='') as csvfile:
                stopwatch_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                stopwatch_writer.writerow([stopwatch.start_time, stopwatch.end_time, stopwatch.get_time_elapsed()])
                
        # Is a file
        elif os.path.isfile(file_name):
            # Is compatible
            with open(file_name, 'a', newline='') as csvfile:
                stopwatch_writer = csv.writer(csvfile, delimiter=',',
                                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
                stopwatch_writer.writerow([stopwatch.start_time, stopwatch.end_time, stopwatch.get_time_elapsed()])
            # Is not compatible
        else:
            # Is a dir
            raise FileNotFound("file not found")

    def read_csv(self, file_name):
        self.set_dir()
        stopwatch_list = []
        if os.path.isfile(file_name):
            if True:#Compatible
                with open(file_name, 'r') as f:
                    csv_reader = csv.reader(f, delimiter=',', quotechar='|')
                    for row in csv_reader:
                        stopwatch = Stopwatch()
                        stopwatch.start_time = int(float(row[0]))
                        stopwatch.end_time = int(float(row[1]))
                        stopwatch_list.append(stopwatch)
            else: #Incompatible
                raise FileNotFound("file not found")
        else:
            raise FileNotFound("file not found")

        return stopwatch_list

    def pretty_print(self, file_name):
        self.set_dir()
        stopwatch_list = self.read_csv(file_name)
        count = 0
        print("\nProject " + file_name + " info")
        print("Start Time          | End Time            | Duration")
        print("====================|=====================|=========================")
        for stopwatch in stopwatch_list:
            count = count + stopwatch.get_time_elapsed()
            print(stopwatch.pretty_start_time() + " | " + stopwatch.pretty_end_time() + " | " + stopwatch.pretty_duration())
        print("Total duration: " + str(timedelta(0, count)))
        
class FileNotFound(Exception):
    pass

class FileNotCompatible(Exception):
    pass

def main():
    stopwatch = Stopwatch()
    csv_manager = CSVManager()
    while True:
        print("\nWhat's your command?")
        command = input()
        if command == 'start':
            stopwatch.start_stopwatch()
        elif command == 'end':
            stopwatch.end_stopwatch()
            print("Project name?")
            name = input()
            csv_manager.write_stopwatch(name, stopwatch)
        elif command == 'pretty':
            print("Project name?")
            name = input()
            csv_manager.pretty_print(name)
        elif command == 'quit':
            break

if __name__ == "__main__":
    main()
