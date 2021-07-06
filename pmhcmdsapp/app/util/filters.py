from app.main import bp
import datetime


@bp.app_template_filter("format_currency")
def format_currency(value):
    if value:
        return "${:,.0f}".format(value)
    else:
        return "$0"

@bp.app_template_filter("format_currency_decimal2")
def format_currency(value):
    if value:
        return "${:,.2f}".format(value)
    else:
        return "$0"

@bp.app_template_filter("format_date")
def format_date(value, defaultpattern="%d/%m/%Y"):
    if isinstance(value,datetime.date):
        return value.strftime(defaultpattern)
    elif not value:
         return ""
    else:
        date_patterns = ["%d/%m/%Y","%Y%m%d","%d-%m-%Y", "%Y-%m-%d","%d/%m/%Y %H:%M","%Y-%m-%d", "%d%m%Y","%Y%m%d"]
        validformat = False
        for pattern in date_patterns:
            try:
                return datetime.datetime.strptime(value, pattern).strftime(defaultpattern)
            except:
                pass
        return ""

@bp.app_template_filter("format_date_mds")
def format_date_mds(value):
    if isinstance(value,datetime.date):
        return "{}{}{}".format(str(value.day).zfill(2),str(value.month).zfill(2),value.year)
    else:
        return ""

@bp.app_template_filter("format_time")
def format_time(value):
    if isinstance(value,datetime.time):
        return "{}:{}".format(str(value.hour).zfill(2),str(value.minute).zfill(2))
    else:
        if not value:
            value = ''
        return value

@bp.app_template_filter("format_string")
def format_string(value):
    if not value:
        return ""
    else:
        return value

@bp.app_template_filter("format_number")
def format_number(value):
    if value == None:
        return ""
    else:
        return value


@bp.app_template_filter("format_year")
def format_year(value):
    if value == None or value == '':
        return ""
    else:
        try:
            year = datetime.datetime.strptime("{}".format(value), "%Y")
        except ValueError:
            return False
        return year.year


