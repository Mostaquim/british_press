from django.db import models
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from streams.blocks import get_all_fields


class HomePage(Page):
    body = StreamField(get_all_fields(), null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]


