import sys
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
  def check(self):
    print('menu')
  
  def __init__(self):
    self.args = sys.argv[1:]
    
  def run_args(self):
    # Make code to handle arguments
    # Check if arugments are valid
    try:
        if len(self.args) != 3:
          raise ValueError(f"Expected 3 arguments, got {len(self.args)}")

        # Convert and validate every argument (must be an integer 1-3)
        for i, arg in enumerate(self.args[:3]):
            try:
                number = int(arg)
            except ValueError:
                raise ValueError(f"Argument {i + 1} ('{arg}') is not a number")
            if number not in (1, 2, 3):
                raise ValueError(f"Argument {i + 1} is {number}, must be 1-3")

        if self.args[0] == 1:
            # Start monitor
            pass
        if self.args[1] == 2:
            # Choose alarm to monitor (cpu, ram, disk)
            pass
        if self.args[2] == 3:
            # Choose monitor limit percentage
            print("works here")

    except ValueError as e:
        print(f"Invalid arguments: {e}")
    
  def run(self):
    # Run standard menu if no arguments are provided
    # kan bli Christians del
    print("Running menu here since no arguments were provided")

  def start(self):
    if len(self.args) > 0:
      self.run_args()
    else:
      # Run a menu that shows options or do something else instead?
      self.run()



