from django.utils.text import slugify
import os, random, string, uuid

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    
    Pclass = instance.__class__
    slug_exists = Pclass.objects.filter(urlSlug=slug).exists()
    if slug_exists:
        new_slug = slugify(slug + ' ' + random_string_generator(size=8))
        return unique_slug_generator(instance, new_slug)
    return slug

def unique_file_path_generator(instance, filename):
    """Generate file path for property image & video"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    filepath = ("uploads/property/{propid}/{proptype}").format(
                    propid=instance.propertyKey.pk, 
                    proptype=instance.mediaType
                )
    return os.path.join(filepath, filename)