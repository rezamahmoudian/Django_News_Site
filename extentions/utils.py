from . import jalali
from django.utils import timezone


def persian_number_convert(mystr):
    numbers = {
        '0': '',
        '1': '',
        '2': '',
        '3': '',
        '4': '',
        '5': '',
        '6': '',
        '7': '',
        '8': '',
        '9': '',
    }



def geregori_to_jalali(time):
    time = timezone.localtime(time)
    geregori_time = '{},{},{}'.format(time.year, time.month, time.day)
    jalali_date = jalali.Gregorian(geregori_time).persian_tuple()
    months = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", " بهمن", "اسفند"
    ]

    output = ' {} {} {}, ساعت {}:{}'.format(jalali_date[2],
                                        months[jalali_date[1]-1],
                                        jalali_date[0],
                                        time.hour,
                                        time.minute
                                          )

    return output

