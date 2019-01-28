"""
Config file for Vrae Vrae
"""

APP_NAME = "Vrae Vrae"
DEFAULT_DATASOURCE = "opentdb"

MAX_TIME_IN_SECONDS: int = 0.1
MAX_QUESTIONS: int = 2
DEFAULT_SCORE: int = 10

# DO NOT EDIT UNDER THIS LINE
DEBUG = False
VERSION = 1.0

POSSIBLE_DATASOURCES = ["opentdb"]
DATASOURCE_PROPERTIES = {"opentdb": {"maxRequest": 50}}
