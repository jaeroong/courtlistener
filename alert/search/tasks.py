# This software and any associated files are copyright 2010 Brian Carver and
# Michael Lissner.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append('/var/www/court-listener/alert')

from alert import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.db.models.signals import post_save
from django.dispatch import receiver

from alert.lib import sunburnt
from alert.search.models import Document
from alert.search.search_indexes import SearchDocument
from celery.decorators import task

si = sunburnt.SolrInterface(settings.SOLR_URL, mode='w')

@task
def delete_docs(docs):
    si.delete(list(docs))
    si.commit()

@task
def add_or_update_docs(docs):
    for doc in docs:
        doc = Document.objects.get(pk=doc)
        search_doc = SearchDocument(doc)
        si.add(search_doc)
        si.commit()

@task
def delete_doc_handler(sender, **kwargs):
    '''Responds to the post_delete signal and deletes the document from the 
    index. See search/__init__.py for the connecting code.
    '''
    si.delete(kwargs['instance'].pk)
    si.commit()

@task
def save_doc_handler(sender, **kwargs):
    '''Responds to the post_save signal and updates the document in the search
    index. See search/__init__.py for the connecting code.
    '''
    search_doc = SearchDocument(kwargs['instance'].pk)
    si.add(search_doc)
    si.commit()