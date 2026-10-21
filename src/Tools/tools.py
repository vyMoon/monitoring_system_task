class Tools:
  toolsMessages = {
    'requestNumber':'Ange ett heltal',
    'errorNumber': 'Du har angett {inp} som inte ser ut som ett tal. Ta en till försök!',
    'betweenStart': 'Välj ett tal mellan {min} och {max}',
    'betweenErr': 'talet är inte mellan {min} och {max}. Ta en försök till.',
    'requestLetter': 'Ange en bokstav',
    'errLetter': '{value} ser inte ut som en bokstav. Ta en försök till!',
  }
def requestNumber(self):
while True:
    inp = input(f'{self.toolsMessages["requestNumber"]} ')
    try:
        number = float(inp) if '.' in inp else int(inp)
    return number
    except:
        print(self.toolsMessages['errorNumber'].format(inp=inp))
        continue

def requestNumberBetween(self, max, min = 0):
    print(self.toolsMessages['betweenStart'].format(min=min, max=max))

    while True:
      number = self.requestNumber()
      if number > max or number < min:
        print(self.toolsMessages['betweenErr'].format(min=min, max=max))
        continue
      return number
