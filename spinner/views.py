import json

from django.shortcuts import render, redirect
from .models import SlugContent, Article, Batch
from .helper import *
from django.core.paginator import Paginator, InvalidPage


def page_generator(request, page=1):
    kwargs = {}
    if request.method == 'POST':
        p = request.POST
        for d in p:
            if d != 'csrfmiddlewaretoken' and p[d]:
                kwargs[d] = p[d]

    pages = SlugContent.objects.using('spinner').filter(**kwargs)

    paginator = Paginator(pages, 100)

    if page > paginator.num_pages:
        page = paginator.num_pages

    if page == 0:
        page = 1

    this_page = paginator.page(page)

    context_pages = page_parser(this_page)

    countries = SlugContent.objects.using(
        'spinner').filter(area_type='country')

    counties = SlugContent.objects.using('spinner').filter(area_type='county')

    hidden_fields = kwargs

    if 'parent_country' in kwargs:
        kwargs['parent_country'] = SlugContent.objects.using(
            'spinner').get(pk=kwargs['parent_country'])

    if 'parent_county' in kwargs:
        kwargs['parent_county'] = SlugContent.objects.using(
            'spinner').get(pk=kwargs['parent_county'])

    context = {
        'next_page': page + 1,
        'prev_page': page - 1,
        'num_page': paginator.num_pages,
        'has_next': this_page.has_next(),
        'has_prev': this_page.has_previous(),
        'pages': context_pages,
        'count': pages.count(),
        'countries': countries,
        'counties': counties,
        'params': kwargs,
        'hidden_fields': hidden_fields
    }

    return render(
        request,
        template_name='spinner/page_generator.html',
        context=context
    )


def create_batch(request):
    if request.method == 'POST':
        kwargs = {}
        count = request.POST['count']
        for d in request.POST:
            if d != 'csrfmiddlewaretoken' and d != 'count' and request.POST[d]:
                kwargs[d] = request.POST[d]
        articles = Article.objects.all()

        kwargs = json.dumps(kwargs)

        context = {
            'count': count,
            'articles': articles,
            'kwargs': kwargs
        }

        return render(
            request,
            template_name='spinner/create_batch.html',
            context=context,
        )
    else:
        return redirect('/admin/spinner/')


def batch(request):
    if request.POST:
        kwargs = request.POST['kwargs']
        name = request.POST['name']
        number = request.POST['number']
        article = request.POST['article']
        article = Article.objects.filter(pk=article)

        if article.exists():
            article = article[0]
            batch = Batch(
                kwargs=kwargs,
                name=name,
                number=number,
                article=article
            )
            batch.save()
            return redirect('/admin/batch/%s/' % batch.pk)
        else:
            return redirect('/admin/spinner/')

    batch = Batch.objects.all()
    context = {
        'batches': batch
    }

    return render(
        request,
        template_name='spinner/batch.html',
        context=context
    )


def batch_view(request, pk):
    batch = Batch.objects.get(pk=pk)
    if batch.started:
        pages = SlugContent.objects.using('spinner').filter(batch=batch.pk)
    else:
        kwargs = json.loads(batch.kwargs)
        kwargs['batch'] = None
        pages = SlugContent.objects.using('spinner').filter(**kwargs)
    context_pages = page_parser(pages)
    context = {
        'batch': batch,
        'pages': context_pages
    }
    return render(
        request,
        template_name='spinner/batch_view.html',
        context=context
    )


def batch_start(request, pk):
    batch = Batch.objects.get(pk=pk)
    kwargs = json.loads(batch.kwargs)
    kwargs['batch'] = None
    pages = SlugContent.objects.using('spinner').filter(**kwargs)
    pages.update(batch=batch.pk)
    batch.started = True
    batch.save()

    return redirect('/admin/batch/%s/' % batch.pk)


def article(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }

    return render(
        request,
        template_name='spinner/article.html',
        context=context
    )


def article_edit(request, pk):
    article = Article.objects.filter(pk=pk)
    if not article.exists():
        return redirect('/admin/article/')

    article = article[0]

    if request.POST:
        article.name = request.POST['name']
        article.content = request.POST['content']
        article.save()

    synoms = get_synoms(article.content)

    context = {
        'article': article,
        'synoms': get_synoms(article.content)
    }

    return render(
        request,
        template_name='spinner/article_edit.html',
        context=context
    )


def article_new(request):
    if request.POST:
        article = Article(
            name=request.POST['name'],
            content=request.POST['content']
        )
        article.save()
        return redirect('/admin/article/%s/' % article.pk)

    context = {}

    return render(
        request,
        template_name='spinner/article_new.html',
        context=context
    )


def article_delete(request, pk):
    article = Article.objects.filter(pk=pk)
    if not article.exists():
        return redirect('/admin/article/')
    article = article[0]
    if request.POST:
        if request.POST['Delete'] == 'true':
            article.delete()
            return redirect('/admin/article/')

    context = {
        'article': article
    }

    return render(
        request,
        template_name='spinner/article_delete.html',
        context=context
    )
