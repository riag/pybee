
import pybee

ask_func = {}


def add_ask_func(ask_type, func):
    assert callable(func)
    global ask_func
    ask_func[ask_type] = func


def get_ask_func(ask_type):
    return ask_func.get(ask_type, None)


def input_str(msg, default_value, allow_empty=True):
    while True:
        p = input(msg)
        if not p and not allow_empty:
            continue

        if not p and allow_empty:
            p = default_value

        return p


def input_password(msg, default_value, allow_empty=True, confirm=True):
    value = pybee.ask.input_password(
        msg, allow_empty, confirm
        )
    if not value and allow_empty:
        value = default_value

    return value


def input_yes_or_no(msg, default_value):
    default = 'yes' if default_value else 'no'
    return pybee.ask.yes_or_no(
        msg, default
    )


def choice(msg, default_value, allow_valus, convert=str):
    m = '%s: ' % msg
    while True:
        p = input(m)
        if not p:
            p = default_value
        p = convert(p)
        if p not in allow_valus:
            continue

        return p


add_ask_func('str', input_str)
add_ask_func('password', input_password)
add_ask_func('yes_or_no', input_yes_or_no)
add_ask_func('choice', choice)
