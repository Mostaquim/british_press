from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from .urls import urlpatterns


@hooks.register('register_admin_menu_item')
def register_spinner_menu_item():
    return MenuItem('Spinner', reverse('spinner'), classnames='icon icon-folder-inverse', order=10000)


@hooks.register('register_admin_menu_item')
def register_article_menu_item():
    return MenuItem('Article', reverse('article'), classnames='icon icon-doc-full', order=10000)


    
@hooks.register('register_admin_menu_item')
def register_article_menu_item():
    return MenuItem('Batch', reverse('batch'), classnames='icon icon-list-ul', order=10000)



@hooks.register('register_admin_urls')
def urlconf_time():
    return urlpatterns
