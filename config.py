"""
Config file for Vrae Vrae
"""

APP_NAME = "Vrae Vrae"
DEFAULT_DATASOURCE = "opentdb"

MAX_TIME_IN_SECONDS: int = 10
MAX_QUESTIONS: int = 10

# DO NOT EDIT UNDER THIS LINE
DEBUG = True
VERSION = 1.0

POSSIBLE_DATASOURCES = ["opentdb"]
DATASOURCE_PROPERTIES = {"opentdb": {"maxRequest": 50}}
