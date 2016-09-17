# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import time, traceback
from sqlalchemy.exc import SQLAlchemyError
from flask import flash, render_template, current_app


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def render_extensions(template_path, **kwargs):
    """
    Wraps around the standard render template method and shoves in some other stuff out of the config.

    :param template_path:
    :param kwargs:
    :return:
    """

    return render_template(template_path,
                           _GOOGLE_ANALYTICS=current_app.config['GOOGLE_ANALYTICS'],
                           **kwargs)


# deal with retry
def retry(try_time):
    def decorator(func):
        def wrapper(*args, **kw):
            attempt = 0
            while attempt < try_time:
                try:
                    return func(*args, **kw)
                except SQLAlchemyError:
                    traceback.print_exc()
                    break
                except Exception:
                    traceback.print_exc()
                    print("Sleep %d seconds and Try more %d times" % (pow(2, attempt + 1), try_time - attempt - 1))
                    attempt += 1
                    time.sleep(pow(2, attempt + 1))
        return wrapper

    return decorator
