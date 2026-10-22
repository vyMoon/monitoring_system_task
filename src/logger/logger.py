from datetime import datetime
from pathlib import Path

class Logger:
  logsFolderName = 'logs'

  def __init__(self, path: Path):
    self.createLogFile(path)

  def createLogFile(self, path: Path):
    now = datetime.now()
    folderPath = path / self.logsFolderName
    folderPath.mkdir(parents=True, exist_ok=True)
    self.filePath = path / self.logsFolderName / f'{now:%Y-%m-%d_%H-%M-%S-%f}.txt'
    self.filePath.touch()

  def log(self, information: str):
    now = datetime.now()
    data = f'{now}: {information}'

    with self.filePath.open('a') as file:
      file.write(f"{data}\n")
      file.close()

  def logPrefix(self, prefix: str, message: str):
    self.log(
      f'{prefix}: {message}'
    )

  def warn(self, message: str):
    self.logPrefix('WARN', message)

  def alarm(self, message: str):
    self.logPrefix('ALARM', message)


# l = Logger(Path.cwd())
# l.log('exempel log')
# l.log('exempel log 2')