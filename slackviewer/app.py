import flask


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


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
