# Login functions for the site

from languages import LANGUAGES
import models

from flask import g
from flask.ext.login import current_user

def get_lang_name(lang_short):
	for value, name in LANGUAGES:
		if value == lang_short:
			return name

def get_short_name(lang_long):
	for value, name in LANGUAGES:
		if name == lang_long:
			return value