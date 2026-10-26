from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from logger.logger import Logger

def get_logger():
  with TemporaryDirectory() as temp_dir:
    path = Path(temp_dir)
    return Logger(path)
    
def test_create_log_file():
  with TemporaryDirectory() as temp_dir:
    path = Path(temp_dir)
    logger = Logger(path)

    log_folder = path / logger.logsFolderName

    assert log_folder.exists()
    assert log_folder.is_dir()
    assert logger.filePath.exists()
    assert logger.filePath.is_file()
    assert logger.filePath.parent == log_folder

test_create_log_file()

def test_logger_log_information():
  with TemporaryDirectory() as temp_dir:
    logger = Logger(Path(temp_dir))
    message = "message"

    logger.log(message)

    with logger.filePath.open("r") as file:
        content = file.read()

    assert message in content
    assert content.endswith("\n")

test_logger_log_information()

def test_logger_log_with_prefix():
  logger = get_logger()
  prefix = 'prefix'
  message = 'message'
  logger.log = Mock()
  logger.logPrefix(prefix, message)
  logger.log.assert_called_with(
    logger.prefixMessage.format(prefix=prefix, message=message)
  )

test_logger_log_with_prefix()

def test_loger_warn():
  logger = get_logger()
  message = 'message'
  logger.logPrefix = Mock()
  logger.warn(message)
  logger.logPrefix.assert_called_with(logger.warnPrefix, message)

test_loger_warn()

def test_loger_alarm():
  logger = get_logger()
  message = 'message'
  logger.logPrefix = Mock()
  logger.alarm(message)
  logger.logPrefix.assert_called_with(logger.alarmPrefix, message)

test_loger_alarm()

print('Tests completed successfully')
