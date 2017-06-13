import click
import functools

from . import config

def login(key, secret):
    c = config.read()
    c['creds'] = [key, secret]
    config.write(c)

def logout():
    c = config.read()
    del c['creds']
    config.write(c)

def credentials():
    c = config.read()
    return c.get('creds')

def pass_client(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj, *args, **kwargs)
    return functools.update_wrapper(new_func, f)
