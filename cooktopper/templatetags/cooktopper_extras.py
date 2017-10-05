from django import template

register = template.Library()

@register.filter
def sub_time(current, old):
	passed_time = current - old
	return '{:02d}m{:02d}s'.format(int(passed_time/60), passed_time%60)
