import pandas as pd
from datetime import datetime
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Raport
from django.shortcuts import redirect


def index(request):
    raports = Raport.objects.all().values()
    raports_data_frame = pd.DataFrame(list(raports))

    raports_data_frame['time_start'] = convert_time_field_to_number(raports_data_frame['time_start'])
    raports_data_frame['time_end'] = convert_time_field_to_number(raports_data_frame['time_end'])
    raports_data_frame['time_diff'] = get_time_dif_from_time_fields(raports_data_frame)
    raports_data_frame['time_diff'] = transform_time_dif_to_minutes_and_int(raports_data_frame)

    grouped_raports = raports_data_frame.groupby(['data'])
    set_sum_of_time_dif_in_time_field(grouped_raports, raports_data_frame)

    context = {'raports': grouped_raports}

    return render(request, 'main_page/index.html', context)


def convert_time_field_to_number(time_field):
    return time_field.apply(lambda x: datetime.strptime(str(x), '%H:%M:%S').time())


def get_time_dif_from_time_fields(time_field):
    return time_field.apply(
        lambda x: datetime.combine(datetime.min, x['time_end']) - datetime.combine(datetime.min, x['time_start']),
        axis=1)


def set_sum_of_time_dif_in_time_field(grouped_data, data_frame):
    for category, group in grouped_data:
        data_frame['total_time'] = group['time_diff'].sum()


def transform_time_dif_to_minutes_and_int(time_field):
    return time_field['time_diff'].apply(lambda x: x.total_seconds() / 60).astype(int)


@require_POST
def add_raport(request):
    data = request.POST['date']
    time_start = request.POST['time_start']
    time_end = request.POST['time_end']
    description = request.POST['description']

    new_raport = Raport(data=data, time_start=time_start, time_end=time_end, description=description)
    new_raport.save()
    return redirect('/')
