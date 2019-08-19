import json
from wagtail.core.models import Page, Orderable
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.blocks import CharBlock
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from django.middleware.csrf import get_token
from .choices import PRODUCT_TYPES
from.helpers import get_product_name


class CatalogPage(Page):
    name = models.CharField(null=False, max_length=200)

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    api_value = models.TextField(null=True)

    page_type = models.CharField(
        max_length=10, choices=PRODUCT_TYPES, default='other')

    list_header = models.TextField(null=True, max_length=500)

    content = RichTextField(null=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_type'),
        FieldPanel('api_value'),
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('list_header'),
        InlinePanel('list_item', label="List"),
        FieldPanel('content')
    ]

    flyer_template = "form/catalog_flyers.html"

    template = "form/catalog.html"

    def get_template(self, request, *args, **kwargs):
        if self.page_type == 'flyer':
            return self.flyer_template
        return self.template

    def save(self, *args, **kwargs):
        self.api_value = json.dumps(json.loads(
            self.api_value), separators=(',', ':'))
        super(CatalogPage, self).save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['csrf'] = get_token(request)
        cache = ApiCache.objects.filter(product=self)
        context['pre_cache'] = {}

        context['product_api_code'] = get_product_name(self.api_value)

        if cache.exists():
            r = json.loads(cache[0].response)
            formats = []
            for i in r['selectGroupList']:
                if i['selectDescription'] == 'a_format':
                    for opt in i['optionList']:
                        tr = opt['optionTranslations']
                        name = None

                        if len(tr) == 3:
                            name = tr[2]
                        if int(tr[0].split()[0]) > int(tr[1].split()[0]):

                            dimension = {
                                'h': int(tr[0].split()[0]) * .7,
                                'w': int(tr[1].split()[0]) * .7
                            }

                        else:
                            dimension = {
                                'h': int(tr[1].split()[0]) * .7,
                                'w': int(tr[0].split()[0]) * .7
                            }

                        o = {
                            'optionName': opt['optionName'],
                            'name': name,
                            'dimension': dimension
                        }

                        if opt['selected']:
                            o['selected'] = True
                        else:
                            o['selected'] = False

                        formats.append(o)

            context['formats'] = formats
            context['select_group'] = r['selectGroupList']
            context['selected'] = r['selected']
        return context


class ListItem(Orderable):
    page = ParentalKey(CatalogPage, related_name='list_item')
    text = models.CharField(null=True, max_length=500)
    panels = [FieldPanel('text')]


class ApiCache(models.Model):
    product = models.ForeignKey(
        CatalogPage, on_delete=models.SET_NULL, null=True)
    response = models.TextField(null=True)
