from django import template
import phonenumbers

register = template.Library()

@register.filter(name="phonenumber")
def phonenumberFormat(value):
    return "+1 {}".format(phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.NATIONAL))

@register.filter(name="filterurl")
def filterCorrectUrl(value, currentfilter):
    if currentfilter:
        currentfilter = currentfilter.replace('.', '')
        currentfilter = list(currentfilter)
        for i in currentfilter:
            if i == str(value):
                currentfilter.remove(i)
                return '.'.join(currentfilter)

        url = "{}.{}".format('.'.join(currentfilter), value)
        return url
    else:
        return value

@register.filter(name="filterclass")
def filterClass(value, currentfilter):
    if currentfilter:
        currentfilter = currentfilter.replace('.', '')
        currentfilter = list(currentfilter)
        for i in currentfilter:
            if i == str(value):
                return True
        return False
    else:
        return False

@register.filter(name="checkboxActive")
def checkboxActive(value):
    if value.data.get('selected', False):
        return True
    return False