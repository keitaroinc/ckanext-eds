"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging

import ckan.logic as l
from sqlalchemy import orm, types, ForeignKey, Column, Table

from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject

log = logging.getLogger(__name__)


__all__ = [
    'UserExtra', 'user_extra_table',
]

user_extra_table = None


def setup():
    if user_extra_table is None:
        define_user_extra_table()
        log.debug('User extra table defined in memory')

        if not user_extra_table.exists():
            user_extra_table.create()
    else:
        log.debug('User extra table already exist')


class UserExtra(DomainObject):
    '''Convenience methods for searching objects
        '''

    @classmethod
    def get(cls, user_id, key, default=None):
        '''Finds a single entity in the register.'''

        kwds = {'user_id': user_id, 'key': key}
        o = Session.query(cls).autoflush(False)
        o = o.filter_by(**kwds).first()
        if o:
            return o
        else:
            return default

    @classmethod
    def delete(cls, user_id, key):
        # Delete single extra
        kwds = {'user_id': user_id, 'key': key}
        obj = Session.query(cls).filter_by(**kwds).first()
        if not obj:
            raise l.NotFound
        Session.delete(obj)
        Session.commit()



def define_user_extra_table():
    global user_extra_table
    user_extra_table = Table('user_extra', metadata,
                             Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
                             Column('user_id', types.UnicodeText, ForeignKey('user.id')),
                             Column('key', types.UnicodeText),
                             Column('value', types.UnicodeText),
                             Column('state', types.UnicodeText, default=u'active'),
                             )

    mapper(
        UserExtra,
        user_extra_table
    )
