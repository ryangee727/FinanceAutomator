import os


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_float_to_dollar(value):
    return '${:,.2f}'.format(value)


def create_archived_month_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
