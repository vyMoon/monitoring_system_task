from datetime import datetime
from pathlib import Path

class Logger:
  # folder name for log files
  logsFolderName = 'logs'

  def __init__(self, path: Path):
    self.createLogFile(path)

  # takes path where logs are stored, create log folder and current log file
  def createLogFile(self, path: Path):
    now = datetime.now()
    folderPath = path / self.logsFolderName
    folderPath.mkdir(parents=True, exist_ok=True)
    self.filePath = path / self.logsFolderName / f'{now:%Y-%m-%d_%H-%M-%S-%f}.txt'
    self.filePath.touch()

  # create line with provided information and  writes it
  def log(self, information: str):
    now = datetime.now()
    data = f'{now}: {information}'

    with self.filePath.open('a') as file:
      file.write(f"{data}\n")
      file.close()

  # log with prefix. line info looks like WARN: cpu current = 80, limit = 85
  def logPrefix(self, prefix: str, message: str):
    self.log(
      f'{prefix}: {message}'
    )

  # logs with warn prefix
  def warn(self, message: str):
    self.logPrefix('WARN', message)

  # logs with alarm prefix
  def alarm(self, message: str):
    self.logPrefix('ALARM', message)


# l = Logger(Path.cwd())
# l.log('exempel log')
# l.log('exempel log 2')