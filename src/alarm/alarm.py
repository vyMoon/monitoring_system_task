import re

alarm_types = ("cpu", "ram" "disk") 

class Alarm:
  name = "Alarm"
  pattern = r'^Alarm - type: (cpu|disk|ram), target: \d+$'

  def __init__(self, alarmType, target =None ):
   if self.isParsAble(alarmType):
    info = self.parseAlarm(alarmType)
    alarmType = info['type']
    target = info['target']

   self.checkType(alarmType)
   self.checkTarget(target)
   self.type = alarmType
   self.target = target

  def __str__(self):
    return f'{self.name} - type: {self.type}, target: {self.target}'
  
  def isParsAble(self, stringified_alarm):
    return bool(re.fullmatch(self.pattern, stringified_alarm))

  def parseAlarm(self, stringified_alarm):
    match = re.search(r"type: *(cpu|disk|ram)", stringified_alarm)
    if match:
      alarmType = match.group(1)
    match = re.search(r"target: *(\d+)", stringified_alarm)
    if match:
      target = match.group(1)
    return {
      'type': alarmType,
      'target': int(target)
    }

  def isBreached(self, value):
    self.validateTargetType(value)
    return value >= self.target

  def validateTargetType(self, target):
    if type(target) is not int and type(target) is not float:
      raise ValueError('Target must be a integer or float')
    return True
  
  def checkType(self, alarmType):
    if alarmType not in alarm_types:
      raise ValueError (
        f"type should be one of cpu,ram,disk {alarmType} provided"
      )

    return True

  def checkTarget(self, target):
    self.validateTargetType(target)
    if target > 100:
      raise ValueError('Target must be more than 0 and not more than 100')
