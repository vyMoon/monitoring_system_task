# Menu
# startar alarm skapande dialog
# options - add alarm, remove alarm, start monitor
# m = Monitor(Alarm(type, target), Alarm(type, target), Alarm(type, target))
# m.start(), m.stop()
# Startar monitor -> m.start()
# avslutar monitors arbete (ctrl c) -> m.stop()
# try:
#   m.start()
# except KeyboardInteruption:
#   m.stop() 
# handlar errors ?

class Menu:
  def check(elf):
    print('menu')
