import logging
from logging.handlers import TimedRotatingFileHandler

levels = {
	'debug': logging.DEBUG,
	'info': logging.INFO,
	'warning': logging.WARNING,
	'error': logging.ERROR,
	'critical': logging.CRITICAL
}


def load_logger(level, path, name):
	"""

	:param level:
	:param path:
	:param name:
	"""
	logger = logging.getLogger()  # set up root logger
	filename = '{0}{1}'.format(path, name)
	handler = TimedRotatingFileHandler(filename, when='H')
	handler.suffix = "%Y-%m-%d.log"
	handler.extMatch = r"^\d{4}-\d{2}-\d{2}\.log$"

	level = levels[level]
	handler.setLevel(level)  # set level for handler
	formatter = '%(asctime)s - %(name)s - %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s'
	handler.setFormatter(logging.Formatter(formatter))
	logger.addHandler(handler)
	logger.setLevel(level)
	return logger
