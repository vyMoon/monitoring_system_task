import sys
import psutil
import itertools
from pathlib import Path
from alarm.alarm import Alarm
from logger.logger import Logger
from typing import Literal, Callable
from datetime import datetime, timedelta

type AlarmType = Literal['cpu', 'ram', 'disk']
type ParameterState = dict[Literal['current', 'limit'], int | float]
type SystemState = dict[AlarmType, ParameterState]

class Monitor:
  spinner = itertools.cycle(['.' * i for i in range(1, 7)])

  def __init__(
      self,
      alarm_path: Path,
      log_path: Path = None,
      monitor_interval = 1,
      alarm_level = 0,
      warn_level = 10
    ):
    self.alarm_path = alarm_path
    self.logger = Logger(log_path) if log_path else None
    self.monitor_interval = monitor_interval
    self.warn_level = warn_level
    self.alarm_level = alarm_level
    self.getStateFn: dict[AlarmType, Callable[[], float]] = {
      'cpu': self.getCpu,
      'ram': self.getRam,
      'disk': self.getDisk,
    }
    self.getAlarms()

  def getAlarms(self):
    with self.alarm_path.open('r') as file:
      data = file.readlines()
      self.alarms = tuple(Alarm(line.strip()) for line in data)

  def startMonitor(self, seconds: int = None):
    if seconds:
      now = datetime.now()
      end = now + timedelta(seconds=seconds)

    while now <= end if seconds else True:
      self.runSpinner()
      state = self.getSystemState()
      for key in state.keys():
        self.logData(key, state[key]['current'], state[key]['limit'])
      now = datetime.now()

  def runSpinner(self):
    sys.stdout.write(
       f"\r\033[K\033[32mMonitoring {next(self.spinner)}\033[0m"
    )
    sys.stdout.flush()

  def logData(self, alarmType: str, state: int | float, limit: int | float):
    if self.logger:
      return self.useLogger(alarmType, state, limit)
    
    print(
      self.getLogStr(alarmType, state, limit)
    )

  def useLogger(self, alarmType: str, state: int | float, limit: int | float):
    delta = limit - state
    logFn = self.logger.log

    if delta <= self.alarm_level:
      logFn = self.logger.alarm
    elif delta <= self.warn_level:
      logFn = self.logger.warn
    
    logFn(
      self.getLogStr(alarmType, state, limit)
    )

  def getLogStr(self, alarmType: str, state: int | float, limit: int | float) -> str:
    return f'{alarmType} - current: {state}, limit: {limit}'
  
  def getCpu(self) -> float:
    return psutil.cpu_percent(interval=self.monitor_interval)

  def getRam(self) -> float:
    return psutil.virtual_memory().percent

  def getDisk(self) -> float:
    return psutil.disk_usage('/').percent
  
  def getSystemState(self) -> SystemState:
    state: SystemState = {}
    for alarm in self.alarms:
      state[alarm.type] = {
        'current': self.getStateFn[alarm.type](),
        'limit': alarm.target
      }
    return state


# m = Monitor(
#   (Path.cwd() / 'alarms' / 'alarms.txt' ),
#   Path.cwd()
# )
# m.startMonitor(60)
