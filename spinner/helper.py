from .models import SlugContent
import re


def page_parser(pages):
    """
        page parser adds the country and county objects
        self -> get self model
        county -> get county model
        country -> get country model
    """
    countries_query = SlugContent.objects.using(
        'spinner').filter(area_type='country')
    counties_query = SlugContent.objects.using(
        'spinner').filter(area_type='county')
    countries = {}
    counties = {}
    for c in countries_query:
        countries[c.pk] = c

    for c in counties_query:
        counties[c.pk] = c

    ps = []
    for p in pages:
        page = {
            'self': p
        }

        if p.parent_country > 0:
            page['country'] = countries[p.parent_country]
        if p.parent_county > 0:
            page['county'] = counties[p.parent_county]

        ps.append(page)

    return ps


def get_synoms(content):
    regex = r"{{(.*?)}}"
    matches = re.finditer(regex, content, re.MULTILINE)
    synoms = []
    for matchNum, match in enumerate(matches, start=1):
        synoms.append({
            'raw': match.group(1),
            'array':  [i.strip() for i in match.group(1).split('|')]
        })

    return synoms
