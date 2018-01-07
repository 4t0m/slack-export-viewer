import flask

######################## HAXXXXX

import os
import webbrowser

import click
import flask

from archive import \
    extract_archive, \
    get_users, \
    get_channels, \
    compile_channels


def envvar(name, default):
    """Create callable environment variable getter

    :param str name: Name of environment variable
    :param default: Default value to return in case it isn't defined
    """
    return lambda: os.environ.get(name, default)


def flag_ennvar(name):
    return os.environ.get(name) == '1'


def configure_app(app, archive):
    # app.debug = debug
    # if app.debug:
    #     print("WARNING: DEBUG MODE IS ENABLED!")
    app.config["PROPAGATE_EXCEPTIONS"] = True

    path = extract_archive(archive)
    user_data = get_users(path)
    channel_data = get_channels(path)
    channels = compile_channels(path, user_data, channel_data)

    top = flask._app_ctx_stack
    top.channels = channels


######################## HAXXXXX


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

configure_app(app, './archive.zip')

@app.route("/channel/<name>")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    root_messages = messages['root_messages']

    return flask.render_template("viewer.html", root_messages=root_messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels))

@app.route("/channel/<name>/<thread_id>")
def channel_thread(name, thread_id):
    messages = flask._app_ctx_stack.channels[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    root_messages = messages['root_messages']
    thread = messages['threads'][thread_id]

    return flask.render_template("viewer.html", root_messages=root_messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 thread=thread)

@app.route("/")
def index():
    channels = list(flask._app_ctx_stack.channels.keys())
    if "general" in channels:
        return channel_name("general")
    else:
        return channel_name(channels[0])
