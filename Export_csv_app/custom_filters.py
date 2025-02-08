from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 'N/A')

import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def get_item(dictionary, key):
    logger.info("get_item filter called")
    return dictionary.get(key, 'N/A')