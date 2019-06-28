# Generated by Django 2.2.2 on 2019-06-24 13:51

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([('intro_block', wagtail.core.blocks.StructBlock([('h1', wagtail.core.blocks.CharBlock(required=True)), ('content', wagtail.core.blocks.TextBlock())])), ('product_block', wagtail.core.blocks.StructBlock([('products', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock('formpage.FormPage')))])), ('BlockWithIcon', wagtail.core.blocks.StructBlock([('h2', wagtail.core.blocks.CharBlock(required=True)), ('icon_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.CharBlock()), ('h3', wagtail.core.blocks.CharBlock()), ('p', wagtail.core.blocks.TextBlock())])))])), ('Text', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())]))], null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
