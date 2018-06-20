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
