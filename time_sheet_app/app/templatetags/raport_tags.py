from django import template

register = template.Library()
increased_value = 0


@register.simple_tag
def increase_value_until_written_out(value):
    global increased_value
    increased_value += value


@register.simple_tag
def print_increased_value():
    global increased_value
    increased_value_copy = increased_value
    increased_value = 0
    return int(increased_value_copy)
