from functools import partial
from .basis import get_two_points_by_time_diff

get_two_points_1min = partial(get_two_points_by_time_diff, 1, 'minutes')
get_two_points_5min = partial(get_two_points_by_time_diff, 5, 'minutes')
get_two_points_10min = partial(get_two_points_by_time_diff, 10, 'minutes')
get_two_points_15min = partial(get_two_points_by_time_diff, 15, 'minutes')
get_two_points_30min = partial(get_two_points_by_time_diff, 30, 'minutes')
get_two_points_1h = partial(get_two_points_by_time_diff, 1, 'hours')
get_two_points_4h = partial(get_two_points_by_time_diff, 4, 'hours')
get_two_points_6h = partial(get_two_points_by_time_diff, 6, 'hours')
get_two_points_12h = partial(get_two_points_by_time_diff, 12, 'hours')
get_two_points_1d = partial(get_two_points_by_time_diff, 1, 'days')
get_two_points_7d = partial(get_two_points_by_time_diff, 7, 'days')
