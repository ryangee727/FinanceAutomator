

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_float_to_dollar(value):
    return '${:,.2f}'.format(value)
