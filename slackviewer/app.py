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
    threads = messages['threads'].items()
    
    return flask.render_template("viewer.html", root_messages=root_messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 threads=threads)


@app.route("/")
def index():
    channels = list(flask._app_ctx_stack.channels.keys())
    if "general" in channels:
        return channel_name("general")
    else:
        return channel_name(channels[0])
