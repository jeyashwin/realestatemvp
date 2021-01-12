from django.utils.text import slugify

from property.utils import random_string_generator

def unique_slug_generator_preference(instance, new_slug=None):
    
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.preferenceType)
    
    Pclass = instance.__class__
    slug_exists = Pclass.objects.filter(preferenceSlug=slug).exists()
    if slug_exists:
        new_slug = slugify(slug + ' ' + random_string_generator(size=8))
        return unique_slug_generator_preference(instance, new_slug)
    return slug