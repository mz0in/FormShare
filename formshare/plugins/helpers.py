"""
Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'request.h'.
"""

import datetime
import logging
import uuid
import arrow
import formshare.plugins as p
import timeago
import validators
from dateutil.parser import parse
from formshare.models import TimeZone
from pattern.en import pluralize as pluralize_en
from pattern.es import pluralize as pluralize_es
from pytz import timezone

log = logging.getLogger("formshare")


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def convert_date(date):
    try:
        if not isinstance(date, datetime.date) and not isinstance(
            date, datetime.datetime
        ):
            if isinstance(date, str):
                if is_date(date):
                    date = parse(date)
                    return date
                else:
                    return None
            else:
                return None
        else:
            return date
    except Exception as e:
        log.error("Error while converting date '{}'. Error: {}".format(date, str(e)))


class HelperAttributeDict(dict):
    """
    This code is based on CKAN
    :Copyright (C) 2007 Open Knowledge Foundation
    :license: AGPL V3.
    """

    def __init__(self, *args, **kwargs):
        super(HelperAttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getitem__(self, key):
        try:
            value = super(HelperAttributeDict, self).__getitem__(key)
        except KeyError:
            raise Exception(
                "Helper function '{key}' has not been defined.".format(key=key)
            )
        return value


# Builtin helper functions.
_builtin_functions = {}
helper_functions = HelperAttributeDict()


def core_helper(f, name=None):
    """
    Register a function as a builtin helper method.

    This code is based on CKAN
        :Copyright (C) 2007 Open Knowledge Foundation
        :license: AGPL V3, see LICENSE for more details.

    """

    def _get_name(func_or_class):
        # Handles both methods and class instances.
        try:
            return func_or_class.__name__
        except AttributeError:
            return func_or_class.__class__.__name__

    _builtin_functions[name or _get_name(f)] = f
    return f


@core_helper
def humanize_date(date, locale="en"):
    """
    This humanize a date.
    :param date: Datetime
    :param locale: Locale code
    :return: A human readble date like "days ago"
    """
    return timeago.format(date, None, locale)


@core_helper
def get_version():
    """
    This returns the version of FormShare
    :return: The version of FormShare
    """
    return "2.32.0 (20231115)"


@core_helper
def month_from_number(month, locale="en", capitalize=True):
    """
    Returns a readable date"
    :param month: Numeric month
    :param locale: Locale code
    :param capitalize: Capitalize month
    :return: A readable date
    """
    if isinstance(month, str):
        if month.isdigit():
            month = int(month)
        else:
            return "NA"
    temp_data = datetime.date(1900, month, 1)
    ar = arrow.get(temp_data)
    month_name = ar.format("MMMM", locale=locale)
    if capitalize:
        month_name = month_name.capitalize()
    return month_name


@core_helper
def readble_date(date, locale="en", timezone_to_use=None):
    """
    Returns a readable date"
    :param date: Datetime
    :param locale: Locale code
    :param timezone_to_use: Timezone to use
    :return: A readable date
    """
    if date is None:
        return "NA"
    date = convert_date(date)
    if date is None:
        return "NA"
    if timezone_to_use is not None:
        date = date.astimezone(timezone(timezone_to_use))
    ar = arrow.get(date)
    if locale == "es":
        return (
            ar.format("dddd d", locale=locale)
            + " de "
            + ar.format("MMMM, YYYY", locale=locale)
        )
    return ar.format("dddd Do of MMMM, YYYY", locale=locale)


@core_helper
def readble_date_with_time(date, locale="en", timezone_to_use=None):
    """
    Returns a readable date"
    :param date: Datetime
    :param locale: Locale code
    :param timezone_to_use: Time zone to use
    :return: A readable date with time
    """
    if date is None:
        return "NA"
    date = convert_date(date)
    if date is None:
        return "NA"
    if timezone_to_use is not None:
        date = date.astimezone(timezone(timezone_to_use))
    ar = arrow.get(date)
    if locale == "es":
        return (
            ar.format("dddd d", locale=locale)
            + " de "
            + ar.format("MMMM, YYYY. HH:mm:ss", locale=locale)
        )
    return ar.format("dddd Do of MMMM, YYYY. HH:mm:ss", locale=locale)


@core_helper
def simple_date(date, timezone_to_use=None):
    """
    Returns a readable date"
    :param date: Datetime
    :param timezone_to_use: Time zone to use
    :return: A si mple date
    """
    if date is None:
        return "NA"
    date = convert_date(date)
    if date is None:
        return "NA"
    if timezone_to_use is not None:
        date = date.astimezone(timezone(timezone_to_use))
    ar = arrow.get(date)
    return ar.format("DD/MM/YYYY")


@core_helper
def simple_date_with_time(date, timezone_to_use=None):
    """
    Returns a readable date"
    :param date: Datetime
    :param timezone_to_use: Time zone to use
    :return: A si mple date
    """
    if date is None:
        return "NA"
    date = convert_date(date)
    if date is None:
        return "NA"
    if timezone_to_use is not None:
        date = date.astimezone(timezone(timezone_to_use))
    ar = arrow.get(date)
    return ar.format("DD/MM/YYYY HH:mm:ss")


@core_helper
def simple_date_usa(date, timezone_to_use=None):
    """
    Returns a readable date"
    :param date: Datetime
    :param timezone_to_use: Time Zone to use
    :return: A readable date
    """
    if date is None:
        return "NA"
    date = convert_date(date)
    if date is None:
        return "NA"
    if timezone_to_use is not None:
        date = date.astimezone(timezone(timezone_to_use))
    ar = arrow.get(date)
    return ar.format("MM/DD/YYYY")


@core_helper
def get_timezone_desc(request, timezone_code):
    """
    Returns the timezone descripcion of a code"
    :param request: Pyramid request object
    :param timezone_code: Timezone code
    :return: Description of timezone
    """
    try:
        res = (
            request.dbsession.query(TimeZone.timezone_name)
            .filter(TimeZone.timezone_code == timezone_code)
            .first()
        )
        return res[0]
    except Exception as e:
        log.error("Error in get_timezone_desc: {}".format(str(e)))
        return "Error"


@core_helper
def get_timezone_offset(request, timezone_code):
    """
    Returns the offset of a timezone"
    :param request: Pyramid request object
    :param timezone_code: Timezone code
    :return: Description of timezone
    """
    try:
        res = (
            request.dbsession.query(TimeZone.timezone_utc_offset)
            .filter(TimeZone.timezone_code == timezone_code)
            .first()
        )
        return res[0]
    except Exception as e:
        log.error("Error in get_timezone_offset: {}".format(str(e)))
        return "Error"


@core_helper
def pluralize(noun, size, locale="en"):
    """
    The function calls connected plugins to expand the pluralize capabilities of FormShare
    :param noun: Noun
    :param size: Size
    :param locale: Locale code
    :return: the plural of a noun based on the locale and size
    """
    if size == 1:
        return noun

    plural = noun

    if locale == "en":
        plural = pluralize_en(noun)
    if locale == "es":
        plural = pluralize_es(noun)

    # Call connected plugins to see if they have extended or overwrite FormShare pluralize function
    for plugin in p.PluginImplementations(p.IPluralize):
        res = plugin.pluralize(noun, locale)
        if res != "":
            plural = res
    # Will return English pluralization if none of the above happens
    # return pluralize_en(noun)
    return plural


@core_helper
def get_setting(
    request, setting_key, default=None
):  # pragma: no cover Cannot be tested due to request object
    """
    Return the gravatar based on a name
    :param request: pyramid request
    :param setting_key: Name for setting to get
    :param default: Default value of the key does not exist
    :return: The value of the setting or None
    """
    return request.registry.settings.get(setting_key, default)


@core_helper
def get_gravatar_url(
    request, name, size=45
):  # pragma: no cover Cannot be tested due to request object
    """
    Return the gravatar based on a name
    :param request: pyramid request
    :param name: Name for the avatar
    :param size: Size of the image
    :return: Gravatar URL
    """
    return request.route_url("gravatar", _query={"name": name, "size": size})


@core_helper
def is_valid_email(email):
    """
    Checks whether the email is valid
    :param email: Email to check
    :return: True of valid otherwise False
    """
    return validators.email(email)


@core_helper
def is_valid_url(url):
    """
    Checks whether the url is valid
    :param url: Url to check
    :return: True of valid otherwise False
    """
    return validators.url(url)


@core_helper
def get_icon_from_mime_type(mime_type):
    """
    Returns the proper font-awesome file icon based on mimetype
    :param mime_type: Mime type
    :return: FontAwesome icon as string
    """
    icon = "far fa-file"
    if mime_type.find("image") >= 0:
        icon = "far fa-file-image"
    if mime_type.find("video") >= 0:
        icon = "far fa-file-video"
    if mime_type.find("audio") >= 0:
        icon = "far fa-file-audio"
    if mime_type == "text/csv":
        icon = "fas fa-file-csv"
    if mime_type == "application/zip":
        icon = "far fa-file-archive"

    return icon


@core_helper
def get_uuid():
    """
    Generates and returns a UUID4
    :return: UUID
    """
    return str(uuid.uuid4())


def load_plugin_helpers():
    """
    (Re)loads the list of helpers provided by plugins.

    This code is based on CKAN
        :Copyright (C) 2007 Open Knowledge Foundation
        :license: AGPL V3, see LICENSE for more details.
    """
    global helper_functions

    helper_functions.clear()
    helper_functions.update(_builtin_functions)

    for plugin in reversed(list(p.PluginImplementations(p.ITemplateHelpers))):
        helper_functions.update(plugin.get_helpers())
