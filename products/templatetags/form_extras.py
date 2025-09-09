from django import template

register = template.Library()

@register.filter
def getitem(dictionary, key):
    """Get item from dictionary using dynamic key"""
    return dictionary.get(key)

@register.filter
def add_str(arg1, arg2):
    """Concatenate two strings"""
    return str(arg1) + str(arg2)

@register.simple_tag
def get_edit_form_errors(session, category_id):
    """Get edit form errors from session"""
    key = f'edit_form_errors_{category_id}'
    return session.get(key, {})

@register.simple_tag
def get_edit_form_data(session, category_id):
    """Get edit form data from session"""
    key = f'edit_form_data_{category_id}'
    return session.get(key, {})