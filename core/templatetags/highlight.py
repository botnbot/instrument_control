import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="highlight")
def highlight(text, search):
    if not search:
        return text

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", str(text))

    return mark_safe(highlighted)
