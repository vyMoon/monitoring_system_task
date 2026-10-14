
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

class Alarm:
  def check(self):
    print('alarm')
    return True
