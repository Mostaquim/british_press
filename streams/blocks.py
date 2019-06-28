from wagtail.core import blocks
from .choices import *


class IntroBlock(blocks.StructBlock):
    h1 = blocks.CharBlock(required=True)
    content = blocks.TextBlock()

    class Meta:
        icon = "placeholder"
        label = "Intro Block"
        template = "stream/intro_block.html"


class ProductBlock(blocks.StructBlock):
    products = blocks.ListBlock(
        blocks.PageChooserBlock('formpage.CatalogPage')
    )

    class Meta:
        icon = 'list-ol'
        template = "stream/product_block.html"
        label = "Products"


class BlockWithIcon(blocks.StructBlock):
    h2 = blocks.CharBlock(required=True)
    icon_block = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('icon', blocks.CharBlock()),
                ('h3', blocks.CharBlock()),
                ('p', blocks.TextBlock()),
            ]
        )
    )

    class Meta:
        icon = 'list-ol'
        template = "stream/block_with_icon.html"
        label = "Block With Icon"


class TextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock()

    class Meta:
        icon = 'placeholder'
        template = "stream/text_block.html"
        label = "RichText"




def get_all_fields():
    return [
        ('intro_block', IntroBlock()),
        ('product_block', ProductBlock()),
        ('BlockWithIcon', BlockWithIcon()),
        ('Text', TextBlock()),
    ]
