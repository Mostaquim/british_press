from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from streams.blocks import NavigationBlock

@register_setting
class NavbarSetting(BaseSetting):
    nav = StreamField(
        [
            ("nav", NavigationBlock()),
        ],
        blank=True, null=True
    )

    products = StreamField(
        [
            ("product",NavigationBlock())
        ]
        ,
        blank=True, null=True
    )

    panels = [
        StreamFieldPanel("nav"),
        StreamFieldPanel("products"),
    ]

