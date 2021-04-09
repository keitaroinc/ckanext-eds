"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from datetime import datetime

from ckan.plugins import toolkit

from ckan.lib.navl.validators import (ignore_missing,
                                      not_empty,
                                      not_missing,
                                      ignore_empty
                                      )

log = logging.getLogger(__name__)


def user_extra_schema():
    return {
        'user_id': [ignore_missing, unicode],
        'key': [not_empty, unicode],
        'value': [not_empty, unicode],
        'state': [ignore_missing, unicode]
    }

def user_extra_delete_schema():
    return {
        'key': [not_empty, unicode]
    }

def user_roles_schema():
    return {
        'user_id': [not_empty, unicode],
        'role': [not_empty, unicode],
    }

def user_roles_delete_schema():
    return {
        'user_id': [not_empty, unicode]
    }

