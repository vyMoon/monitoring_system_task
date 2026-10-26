from pathlib import Path
from tempfile import TemporaryDirectory
from monitor.monitor import Monitor
from unittest.mock import patch, Mock, call
from datetime import datetime 

def getAlarms():
  return 'Alarm - type: cpu, target: 5\nAlarm - type: disk, target: 30\nAlarm - type: ram, target: 50'
def getNoCpuAlarms():
  return 'Alarm - type: disk, target: 30\nAlarm - type: ram, target: 50'
def getCpuAlarm():
  return 'Alarm - type: cpu, target: 5'
def getRamAlarm():
  return 'Alarm - type: ram, target: 50'
def getDiskAlarm():
  return 'Alarm - type: disk, target: 30'

def getMonitor():
  with TemporaryDirectory() as temp_dir:
    alarm_path = Path(temp_dir) / "alarms.txt"
    alarm_path.write_text(
      getAlarms()
    )

    return Monitor(alarm_path)

def test_monitor_has_been_created():
  with TemporaryDirectory() as temp_dir:
    alarm_path = Path(temp_dir) / "alarms.txt"
    alarm_path.write_text(
      getAlarms()
    )

    monitor = Monitor(alarm_path)

    assert monitor.alarm_path == alarm_path
    assert monitor.logger is None
    assert monitor.monitor_interval == 1
    assert monitor.alarm_level == 0
    assert monitor.warn_level == 10

test_monitor_has_been_created()

def test_monitor_set_has_cpu_alarm():
  with TemporaryDirectory() as temp_dir:
    alarm_path = Path(temp_dir) / "alarms.txt"
    alarm_path.write_text(
      getAlarms()
    )

    monitor = Monitor(alarm_path)
    assert monitor.hasCpuAlarm == True

    alarm_path.write_text(
      getNoCpuAlarms()
    )

    monitor = Monitor(alarm_path)
    assert monitor.hasCpuAlarm == False

test_monitor_set_has_cpu_alarm()

def test_get_cpu():
  procent = 25.0
  with patch('monitor.monitor.psutil.cpu_percent', return_value=procent) as mock_cpu:
    monitor = getMonitor()
    assert monitor.getCpu() == procent
    mock_cpu.assert_called_once_with(interval=monitor.monitor_interval)

test_get_cpu()

def test_get_ram():
  procent = 60.0
  with patch('monitor.monitor.psutil.virtual_memory', return_value=Mock(percent=procent)) as mock_ram:
    monitor = getMonitor()
    assert monitor.getRam() == procent
    mock_ram.assert_called_once_with()

test_get_ram()

def test_get_disk():
  procent = 78.0
  with patch('monitor.monitor.psutil.disk_usage', return_value=Mock(percent=procent)) as mock_disk:
    monitor = getMonitor()
    assert monitor.getDisk() == procent
    mock_disk.assert_called_once_with('/')

test_get_disk()

def test_get_system_state():
  cpuTarget = 10
  ramTarget = 20
  diskTarget = 30
  cpuCurrent = 40
  ramCurrent = 50
  diskCurrent = 60
  monitor = getMonitor()
  monitor.alarms = (
    Mock(type='cpu', target=cpuTarget),
    Mock(type='ram', target=ramTarget),
    Mock(type='disk', target=diskTarget)
  )

  with patch.object(monitor, 'getCpu', return_value=cpuCurrent) as mock_cpu, \
    patch.object(monitor, 'getRam', return_value=ramCurrent) as mock_ram, \
    patch.object(monitor, 'getDisk', return_value=diskCurrent) as mock_disk:

      monitor.getStateFn['cpu'] = monitor.getCpu
      monitor.getStateFn['ram'] = monitor.getRam
      monitor.getStateFn['disk'] = monitor.getDisk

      state = monitor.getSystemState()

      assert state == {
        'cpu': {'current': cpuCurrent, 'limit': cpuTarget},
        'ram': {'current': ramCurrent, 'limit': ramTarget},
        'disk': {'current': diskCurrent, 'limit': diskTarget},
      }

      mock_cpu.assert_called_once()
      mock_ram.assert_called_once()
      mock_disk.assert_called_once()

test_get_system_state()

def text_monitor_chose_log_method():
  logger = Mock()
  logger.log = Mock()
  logger.warn = Mock()
  logger.alarm = Mock()
  monitor = getMonitor()
  monitor.logger = logger

  fn = monitor.getLogFnByDelta(30)
  assert fn == logger.log
  fn = monitor.getLogFnByDelta(5)
  assert fn == logger.warn
  fn = monitor.getLogFnByDelta(0)
  assert fn == logger.alarm

text_monitor_chose_log_method()

def test_monitor_creates_logString():
  alarmType = 'type'
  state = 10
  limit =  20
  monitor = getMonitor()
  string = monitor.getLogStr(alarmType, state, limit)

  assert string == monitor.logStr.format(alarmType=alarmType, state=state, limit=limit)

test_monitor_creates_logString()

def test_monitor_use_logger():
  alarmType = 'type'
  state = 10
  limit =  20
  monitor = getMonitor()
  logFn = Mock()
  logStr = 'log string'

  with patch.object(monitor, 'getLogFnByDelta', return_value = logFn) as mock_get_log_fn, \
      patch.object(monitor, 'getLogStr', return_value = logStr) as mock_get_str:
    monitor.useLogger(alarmType, state, limit)

    mock_get_log_fn.assert_called_with(limit - state)
    mock_get_str.assert_called_with(alarmType, state, limit)
    logFn.assert_called_with(logStr)

test_monitor_use_logger()

def test_monitor_use_print():
  alarmType = 'type'
  state = 10
  limit =  20
  logStr = 'log string'
  monitor = getMonitor()

  with patch('builtins.print') as mock_print, \
      patch.object(monitor, 'getLogStr', return_value=logStr) as mock_getLogStr:
    monitor.consoleLog(alarmType, state, limit)

    mock_getLogStr.assert_called_with(alarmType, state, limit)
    mock_print.assert_called_with(logStr)

test_monitor_use_print()

def test_monitor_log_data():
  alarmType = 'type'
  state = 10
  limit =  20
  logger = Mock()
  monitor = getMonitor()

  with patch.object(monitor, 'consoleLog') as mock_console, \
      patch.object(monitor, 'useLogger') as mock_logger:
    monitor.logData(alarmType, state, limit)
    mock_console.assert_called_with(alarmType, state, limit)

    monitor.logger = logger
    monitor.logData(alarmType, state, limit)
    mock_logger.assert_called_with(alarmType, state, limit)

test_monitor_log_data()


def test_run_spinner():
  monitor = getMonitor()

  with patch('monitor.monitor.sys.stdout.write') as mock_write, \
      patch('monitor.monitor.sys.stdout.flush') as mock_flush:

    monitor.spinner = iter(['.'])
    monitor.runSpinner()

    mock_write.assert_called_once_with('\r\033[K\033[32mMonitoring .\033[0m')
    mock_flush.assert_called_once_with()

test_run_spinner()

def test_monitorSystem():
  cpuKey = 'cpu'
  ramKey = 'ram'
  cpuCurrent = 10
  cpuLimit = 20
  ramCurrent = 30
  ramLimit = 40

  monitor = getMonitor()
  state = {
    cpuKey: {'current': cpuCurrent, 'limit': cpuLimit},
    ramKey: {'current': ramCurrent, 'limit': ramLimit},
  }

  with patch.object(monitor, 'getSystemState', return_value=state), \
      patch.object(monitor, 'logData') as mock_logData:

    monitor.monitorSystem()

    assert mock_logData.call_args_list == [
      call('cpu', cpuCurrent, cpuLimit),
      call('ram', ramCurrent, ramLimit),
    ]

test_monitorSystem()

def test_startMonitor():
  monitor = getMonitor()

  with patch('monitor.monitor.datetime') as mock_datetime, \
      patch.object(monitor, 'runSpinner') as mock_spinner, \
      patch.object(monitor, 'monitorSystem') as mock_monitorSystem:

    mock_datetime.now.side_effect = [
      datetime(2025, 1, 1, 0, 0, 0),
      datetime(2025, 1, 1, 0, 0, 2),
    ]

    monitor.startMonitor(seconds=1)
    mock_monitorSystem.assert_called_once()
    mock_spinner.assert_called_once()

test_startMonitor()

print('Tests completed successfully')