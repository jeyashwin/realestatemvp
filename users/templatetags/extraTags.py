from django import template
import phonenumbers

register = template.Library()

@register.filter(name="phonenumber")
def phonenumberFormat(value):
    return "+1 {}".format(phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.NATIONAL))