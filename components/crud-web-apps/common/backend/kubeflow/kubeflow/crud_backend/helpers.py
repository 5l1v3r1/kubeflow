"""
Common helper functions for handling k8s objects information
"""
import datetime as dt
import logging

import yaml

log = logging.getLogger(__name__)


def load_yaml(f):
    """
    f: file path
    Load a yaml file and convert it to a python dict.
    """
    c = None
    try:
        with open(f, "r") as yaml_file:
            c = yaml_file.read()
    except IOError:
        log.error(f"Error opening: {f}")
        return None

    try:
        contents = yaml.safe_load(c)
        if contents is None:
            # YAML exists but is empty
            return {}
        else:
            # YAML exists and is not empty
            return contents
    except yaml.YAMLError:
        return None


def load_param_yaml(f, **kwargs):
    """
    f: file path

    Load a yaml file and convert it to a python dict. The yaml might have some
    `{var}` values which the user will have to format. For this we first read
    the yaml file and replace these variables and then convert the generated
    string to a dict via the yaml module.
    """
    c = None
    try:
        with open(f, "r") as yaml_file:
            c = yaml_file.read().format(**kwargs)
    except IOError:
        log.error(f"Error opening: {f}")
        return None

    try:
        contents = yaml.safe_load(c)
        if contents is None:
            # YAML exists but is empty
            return {}
        else:
            # YAML exists and is not empty
            return contents
    except yaml.YAMLError:
        return None


def get_uptime(then):
    """
    then: datetime instance | string

    Return a string that informs how much time has pasted from the provided
    timestamp.
    """
    if isinstance(then, str):
        then = dt.datetime.strptime(then, "%Y-%m-%dT%H:%M:%SZ")

    now = dt.datetime.now()
    diff = now - then.replace(tzinfo=None)

    days = diff.days
    hours = int(diff.seconds / 3600)
    mins = int((diff.seconds % 3600) / 60)

    age = ""
    if days > 0:
        if days == 1:
            age = str(days) + " day"
        else:
            age = str(days) + " days"
    else:
        if hours > 0:
            if hours == 1:
                age = str(hours) + " hour"
            else:
                age = str(hours) + " hours"
        else:
            if mins == 0:
                return "just now"
            if mins == 1:
                age = str(mins) + " min"
            else:
                age = str(mins) + " mins"

    return age + " ago"


def get_age(k8s_object):
    """
    k8s_object: k8s custom resource | dictionary

    Return a dictionary that contains the creationTimestamp (timestamp) of the
    given k8s object and the amount of time that has passed from that timestamp
    (uptime).
    """
    return {
        "uptime": get_uptime(
            k8s_object["metadata"]["creationTimestamp"]),
        "timestamp": k8s_object["metadata"]["creationTimestamp"],
    }
