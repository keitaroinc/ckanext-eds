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

import ckan.logic as l
from sqlalchemy import orm, types, ForeignKey, Column, Table

from ckan.model.meta import metadata, mapper, Session
from ckan.model.types import make_uuid
from ckan.model.domain_object import DomainObject

log = logging.getLogger(__name__)


__all__ = [
    'UserRoles', 'user_roles_table',
]

user_roles_table = None


def setup():
    if user_roles_table is None:
        define_user_roles_table()
        log.debug('User roles table defined in memory')

        if not user_roles_table.exists():
            user_roles_table.create()
    else:
        log.debug('User roles table already exist')


class UserRoles(DomainObject):
    '''Convenience methods for searching objects
        '''

    @classmethod
    def get(cls, user_id):
        '''Finds the role of a given user'''

        kwds = {'user_id': user_id}
        o = Session.query(cls).autoflush(False)
        o = o.filter_by(**kwds).first()
        if o:
            return o
        else:
            return False

    @classmethod
    def delete(cls, user_id):
        '''Removes a given users role'''
        kwds = {'user_id': user_id}
        obj = Session.query(cls).filter_by(**kwds).first()
        if not obj:
            raise l.NotFound
        Session.delete(obj)
        Session.commit()



def define_user_roles_table():
    global user_roles_table
    user_roles_table = Table('user_roles', metadata,
                             Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
                             Column('user_id', types.UnicodeText, ForeignKey('user.id')),
                             Column('role', types.UnicodeText),
                             )

    mapper(
        UserRoles,
        user_roles_table
    )

