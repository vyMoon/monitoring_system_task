import psutil
from pathlib import Path
from alarm.alarm import Alarm
from datetime import datetime, timedelta

class Monitor:
  def __init__(self, alarm_path, monitor_interval = 1):
    self.alarm_path = alarm_path
    self.monitor_interval = monitor_interval
    self.getAlarms()
    self.getStateFn = {
      'cpu': self.getCpu,
      'ram': self.getRam,
      'disk': self.getDisk,
    }

  def getAlarms(self):
    with self.alarm_path.open('r') as file:
      data = file.readlines()
      self.alarms = tuple(Alarm(line.strip()) for line in data)

  def startMonitor(self, seconds = None):
    if seconds:
      now = datetime.now()
      end = now + timedelta(seconds=seconds)

    while now <= end if seconds else True:
      state = self.getSystemState()
      for key in state.keys():
        print(f'{key} - current: {state[key]['current']}, limit: {state[key]['limit']}')
      now = datetime.now()

  def getCpu(self):
    return psutil.cpu_percent(interval=self.monitor_interval)

  def getRam(self):
    return psutil.virtual_memory().percent

  def getDisk(self):
    return psutil.disk_usage('/').percent
  
  def getSystemState(self):
    state = {}
    for alarm in self.alarms:
      state[alarm.type] = {
        'current': self.getStateFn[alarm.type](),
        'limit': alarm.target
      }
    return state


m = Monitor(
  (Path.cwd() / 'alarms' / 'alarms.txt' )
)
m.startMonitor(5)
