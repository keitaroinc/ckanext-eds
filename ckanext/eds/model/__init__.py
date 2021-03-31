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

import vdm.sqlalchemy
from vdm.sqlalchemy.base import SQLAlchemySession

from datetime import datetime

import ckan.model.meta as meta
from ckan.model.package import Package
from ckan.model.tag import PackageTag
from ckan.model.resource import Resource
from ckan.model.package_extra import PackageExtra
from ckan.model.group import (
    Member,
    Group
)
from ckan.model.system_info import SystemInfo


class RepositoryEds(vdm.sqlalchemy.Repository):

    def purge_revision(self, revision, leave_record=False):
        '''Purge revisions.'''

        SQLAlchemySession.setattr(self.session, 'revisioning_disabled', True)
        self.session.autoflush = False
        for o in self.versioned_objects:
            revobj = o.__revision_class__
            items = self.session.query(revobj). \
                filter_by(revision=revision).all()
            for item in items:
                self.session.delete(item)
        if leave_record:
            revision.message = u'PURGED: %s' % datetime.now()
        else:
            self.session.delete(revision)
        self.commit_and_remove()


repo_eds = RepositoryEds(meta.metadata, meta.Session,
                  versioned_objects=[Package, PackageTag, Resource,
                                     PackageExtra, Member,
                                     Group, SystemInfo]
                  )
