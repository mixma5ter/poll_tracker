from django import template
register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def add_score_range(field, model):
    return field.as_widget(attrs={'min': model.min_score, 'max': model.max_score})
