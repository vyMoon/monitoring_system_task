import math
import re

alarm_types = ("cpu", "ram", "disk") 

# Class Alarm
# used in monitor class in order to check if the level of usage is more than the target
# type - monitor object. string There is three types ram, cpu disk
# target - integer\float min - 0, max - 100
# level of usage when alarm should be shown
# usage Alarm(type, target) Alarm('cpu', 50)
# constructor can take a string like 'Alarm - type: cpu, target: 40' as the first  argument
# if possible the string will be parsed to values and continue working with them
# string 'Alarm - type: cpu, target: 40' is exactly the string that
# method __str__() return, so it make it easier to write alarms into a file
# then read alarm from the file and provide them to a constructor
# DO NOT FORGET REMOVING Carriage return (\n)
class Alarm:
  name = "Alarm"
  # regexp to check if it is possible to parse type 
  pattern = r'^Alarm - type: (cpu|disk|ram), target: \d+$'

  def __init__(self, alarmType, target = None):
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

  # check if it is possible to parse type argument
  def isParsAble(self, stringified_alarm):
    return bool(re.fullmatch(self.pattern, stringified_alarm))

  # parse string, return a dictionary with fields type and target
  def parseAlarm(self, stringified_alarm):
    # check ti there is correct type and gets it
    match = re.search(r"type: *(cpu|disk|ram)", stringified_alarm)
    if match:
      alarmType = match.group(1)
    # check if there is correct target and returns it
    match = re.search(r"target: *(\d+)", stringified_alarm)
    if match:
      target = match.group(1)
    return {
      'type': alarmType,
      'target': int(target)
    }

  # check the type of value, if it comparable with the target
  #  if the level of usage more than provided target
  def isBreached(self, value):
    self.validateTargetType(value)
    return value >= self.target

  # check if the provided type of target is int or float 
  def validateTargetType(self, target):
    if type(target) is not int and type(target) is not float:
      raise ValueError('Target must be a integer or float')
    return True

  # check if the type one available types cpu\ram\disk
  def checkType(self, alarmType):
    if alarmType not in alarm_types:
      raise ValueError (
        f"type should be one of cpu,ram,disk {alarmType} provided"
      )

    return True

  # check the type and value of provided target
  def checkTarget(self, target):
    self.validateTargetType(target)
    if target < 0 or target > 100 or not math.isfinite(target):
      raise ValueError('Target must be between 0 and 100')
