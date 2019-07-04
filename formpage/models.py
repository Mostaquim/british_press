import json
from wagtail.core.models import Page, Orderable
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.blocks import CharBlock
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from django.middleware.csrf import get_token
from api.models import ApiCache


class CatalogPage(Page):
    name = models.CharField(null=False, max_length=200)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    api_value = models.CharField(null=True, max_length=200)

    list_header = models.TextField(null=True, max_length=500)

    content = RichTextField(null=True)

    content_panels = Page.content_panels + [
        FieldPanel('api_value'),
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('list_header'),
        InlinePanel('list_item', label="List"),
        FieldPanel('content')
    ]

    template = "form/catalog.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['csrf'] = get_token(request)
        cache = ApiCache.objects.filter(product=self.api_value)
        context['pre_cache'] = {}
        if cache.exists():
            r = json.loads(cache[0].response)
            context['select_group'] = r['selectGroupList']
            context['selected'] = r['selected']
        return context


class ListItem(Orderable):
    page = ParentalKey(CatalogPage, related_name='list_item')
    text = models.CharField(null=True, max_length=500)
    panels = [FieldPanel('text')]
