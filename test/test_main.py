from context import main
Stopwatch = main.Stopwatch
CSVManager = main.CSVManager

import time
import pytest
import os
import csv

from unittest.mock import Mock, patch, mock_open

def test_inital_stopwatch():
    stopwatch = Stopwatch()
    assert stopwatch.start_time == -1
    assert stopwatch.end_time == -1
    assert stopwatch.is_stopwatch_on == False

def test_inital_stopwatch_with_parameters():
    stopwatch = Stopwatch(100, 100, True)
    assert stopwatch.start_time == 100
    assert stopwatch.end_time == 100
    assert stopwatch.read_only == True
    
@patch('time.time', return_value = 100)
def test_start_stopwatch(mock_time):
    stopwatch = Stopwatch()
    stopwatch.start_stopwatch()
    assert stopwatch.start_time == 100
    assert stopwatch.is_stopwatch_on == True

def test_start_stopwatch_when_end_time():
    stopwatch = Stopwatch()
    stopwatch.end_time = 100
    stopwatch.start_stopwatch()
    assert stopwatch.end_time == -1

def test_start_stopwatch_with_read_only():
    with pytest.raises(main.StopwatchReadOnly) as excinfo:
        stopwatch = Stopwatch()
        stopwatch.read_only = True
        stopwatch.start_stopwatch()
        assert "stopwatch is set to read only" in str(excinfo.value)

@patch('time.time', return_value = 100)
#@patch('__main__.Stopwatch.is_stopwatch_on', return_value = False)
def test_end_stopwatch_when_stopwatch_is_off(mock_time):#, mock_is_on):
    with pytest.raises(main.StopwatchNotOn) as excinfo:
        stopwatch = Stopwatch()
        ## How do I test this one correctly?
        stopwatch.is_stopwatch_on = False
        stopwatch.end_stopwatch()
        assert "stopwatch not on" in str(excinfo.value)

@patch('time.time', return_value = 100)
def test_end_stopwatch_when_stopwatch_is_on(mock_time):
    stopwatch = Stopwatch()
    stopwatch.is_stopwatch_on = True
    stopwatch.end_stopwatch()
    assert stopwatch.end_time == 100
    assert stopwatch.is_stopwatch_on == False

def test_end_stopwatch_with_read_only():
    with pytest.raises(main.StopwatchReadOnly) as excinfo:
        stopwatch = Stopwatch()
        stopwatch.read_only = True
        stopwatch.end_stopwatch()
        assert "stopwatch is set to read only" in str(excinfo.value)
    
def get_time_elapsed_when_stopped():
    stopwatch = Stopwatch()
    stopwatch.is_stopwatch_on = False
    stopwatch.start_time = 100
    stopwatch.end_time = 230
    assert stopwatch.get_time_elapsed() == 130

@patch('time.time', return_value = 230)
def get_time_elapsed_when_still_running(mock_time):
    stopwatch = Stopwatch()
    stopwatch.is_stopwatch_on = True
    stopwatch.start_time = 100
    assert stopwatch.get_time_elapsed() == 130

def get_time_elapsed_when_never_started():
    with pytest.raises(main.StopwatchNotStarted) as excinfo:
        stopwatch = Stopwatch()
        stopwatch.start_time = -1
        assert "stopwatch not started" in str(excinfo.value)

################################################################################

def test_inital_CSVManager_with_default_path(tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path / 'projects'

    csv_manager = CSVManager()
    assert csv_manager.default_path == './projects'
    assert os.path.exists(os.path.abspath(csv_manager.default_path)) == True
    assert os.path.isdir(os.path.abspath(csv_manager.default_path)) == True

def test_inital_CSVManager_with_existing_path(tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path / 'test'
    
    csv_manager = CSVManager(default_path = "./test")
    assert csv_manager.default_path == "./test"
    assert os.path.exists(os.path.abspath(csv_manager.default_path)) == True
    assert os.path.isdir(os.path.abspath(csv_manager.default_path)) == True

def test_inital_CSVManager_with_new_path(tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path
    csv_manager = CSVManager(default_path = "./does_not_exist")

    assert csv_manager.default_path == './does_not_exist'
    assert os.path.exists(os.path.abspath(csv_manager.default_path)) == True
    assert os.path.isdir(os.path.abspath(csv_manager.default_path)) == True
    
## Lets ignore an incorrect file type for now
def test_write_stopwatch_with_incorrect_file(tmp_path):
    pass    

def test_write_stopwatch_with_existing_file(tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path
    with open("./exists.csv", 'w+', newline='') as csvfile:
        stopwatch_writer = csv.writer(csvfile, delimiter=',',
                                      quotechar='|', quoting=csv.QUOTE_MINIMAL)
        stopwatch_writer.writerow([200,300,100])

    stopwatch = Stopwatch()
    stopwatch.start_time = 100
    stopwatch.end_time = 200

    csv_manager = CSVManager(default_path = str(test_path))
    csv_manager.write_stopwatch('./exists.csv', stopwatch)

    with open('./exists.csv', mode='r') as f:
        assert f.read() == "200,300,100\n100,200,100\n"
    
def test_write_csv_with_new_file(tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path
    
    stopwatch = Stopwatch()
    stopwatch.start_time = 100
    stopwatch.end_time = 200

    csv_manager = CSVManager(default_path = str(test_path))
    csv_manager.write_stopwatch("./new.csv", stopwatch)

    with open(str(test_path) + '/new.csv', mode='r') as f:
        assert f.read() == "100,200,100\n"

@patch('os.path.isfile', return_value = True)
#@patch('os.open', return_value = "100,200,100\n")
@patch('builtins.open', mock_open(read_data="100,200,100\n"))
def test_read_csv_with_existing_file_with_one_rows(mock_isfile, tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path / 'projects'
    
    stopwatch = Stopwatch()
    stopwatch.start_time = 100
    stopwatch.end_time = 200
    
    csv_manager = CSVManager()
    stopwatch_list = csv_manager.read_csv('test_proj.csv')
    assert stopwatch_list[0].start_time == stopwatch.start_time
    assert stopwatch_list[0].end_time == stopwatch.end_time
        
@patch('os.path.isfile', return_value = True)
#@patch('os.open', return_value = "100,200,100\n200,300,100\n")
@patch('builtins.open', mock_open(read_data="100,200,100\n200,300,100\n"))
def test_read_csv_with_existing_file_with_multiple_rows(mock_isfile, tmp_path):
    os.chdir(tmp_path)
    test_path = tmp_path / 'projects'
    
    stopwatch = Stopwatch()
    stopwatch.start_time = 100
    stopwatch.end_time = 200
    
    stopwatch1 = Stopwatch()
    stopwatch1.start_time = 200
    stopwatch1.end_time = 300
    
    csv_manager = CSVManager()
    stopwatch_list = csv_manager.read_csv('test_proj.csv')

    assert stopwatch_list[0].start_time == stopwatch.start_time
    assert stopwatch_list[0].end_time == stopwatch.end_time
    assert stopwatch_list[1].start_time == stopwatch1.start_time
    assert stopwatch_list[1].end_time == stopwatch1.end_time
    
def test_read_csv_with_existing_incompatible_file():
    pass

def test_read_csv_with_new_file():
    with pytest.raises(main.FileNotFound) as excinfo:
        csv_manager = CSVManager()
        csv_manager.read_csv('test_proj.csv')
        assert "file not found" in str(excinfo.value)

# Kinda a pain to test properly, need to go out and find unixtimes.
def test_pretty_print_csv():
    pass
