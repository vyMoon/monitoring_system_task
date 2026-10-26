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
  # the set of symbols that are shown in the console during monitoring
  spinner = itertools.cycle(['.' * i for i in range(1, 7)])

  def __init__(
      self,
      # path to alarm file
      alarm_path: Path,
      # path to log folder
      log_path: Path = None,
      # spu demands monitoring interval
      monitor_interval = 1,
      # delta current - alarm value. used in making decision what log function used (standard, warn or alarm)
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

  # check alarms file and get alarms
  def getAlarms(self):
    with self.alarm_path.open('r') as file:
      data = file.readlines()
      self.alarms = tuple(Alarm(line.strip()) for line in data)

      if not len(self.alarms):
        raise ValueError('Not possible to start monitoring with no alarms')

  def checkCpuAlarm(self):
    for alarm in self.alarms:
      if alarm.type == 'cpu':
        self.hasCpu = True
  # takes monitoring time in seconds, if not provided permanent monitor
  def startMonitor(self, seconds: int = None):
    if seconds:
      now = datetime.now()
      end = now + timedelta(seconds=seconds)

    while now <= end if seconds else True:
      self.runSpinner()
      self.monitorSystem()
      now = datetime.now()

  # gather information about the system and log it
  def monitorSystem(self):
    state = self.getSystemState()
    for key in state.keys():
      self.logData(key, state[key]['current'], state[key]['limit'])

  # change spinner in the console
  def runSpinner(self):
    sys.stdout.write(
       f"\r\033[K\033[32mMonitoring {next(self.spinner)}\033[0m"
    )
    sys.stdout.flush()

  # logg data in file if the path provided, otherwise log in the console
  def logData(self, alarmType: str, state: int | float, limit: int | float):
    if self.logger:
      self.useLogger(alarmType, state, limit)
      return
    self.consoleLog(alarmType, state, limit)

  # print out the information in the console
  def consoleLog(self, alarmType, state, limit):
    print(
      self.getLogStr(alarmType, state, limit)
    )

  # prints the information to a file
  def useLogger(self, alarmType: str, state: int | float, limit: int | float):
    delta = limit - state
    logFn = self.getLogFnByDelta(delta)
    logFn(
      self.getLogStr(alarmType, state, limit)
    )

  # chose which funktion is used normal log, warn log or alarm log
  def getLogFnByDelta(self, delta: int | float) -> Callable[[str], None]:
    if delta <= self.alarm_level:
      return self.logger.alarm
    elif delta <= self.warn_level:
      return self.logger.warn
    return self.logger.log

  # returns correct information string for logging 
  def getLogStr(self, alarmType: str, state: int | float, limit: int | float) -> str:
    return f'{alarmType} - current: {state}, limit: {limit}'

  # returns current cpu state
  def getCpu(self) -> float:
    return psutil.cpu_percent(interval=self.monitor_interval)

  # # returns current ram state
  def getRam(self) -> float:
    return psutil.virtual_memory().percent

  # returns current disk state
  def getDisk(self) -> float:
    return psutil.disk_usage('/').percent

  # gather all the information to the system state dict.
  # keys -> alarm types
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
# m.startMonitor(10)
