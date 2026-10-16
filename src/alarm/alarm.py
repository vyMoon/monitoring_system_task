
# Alarm
# Innehåler imformation om  alarmet
# disk, ram, cpu
# har check method som tar värde och jämför med värde som fik

# Alarm(type, target) Alarm('cpu': string, 500:int)
# ser till att type är sträng och
# target är percent from 0 ? to 100 integer(float??) annars rise error
# types = 'cpu' \ 'ram' \ disk

# check method kollar på om argumenten är lägre högre elle lika med target
# om lägre returnera false annars true

alarm_types = ("cpu", "ram" "disk") 

class Alarm:
  name = "Alarm"

  def __init__(self, alarmtype, target ):
   self.checkType(alarmtype)
   self.type = alarmtype
   self.target = target
  

  def checkType(self, alarmtype):
    print (alarmtype)
    if alarmtype not in alarm_types:
      raise ValueError ("type should be one of cpu,ram,disk")

    return True

  def checkTarget(self, target):
    if target > 100:
      raise ValueError



a = Alarm("cpu", 50)
