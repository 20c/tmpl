def get_engine(name):
    """
    get an engine from string (engine class without Engine)
    """

    name = name.capitalize() + "Engine"
    if name in globals():
        return globals()[name]

    raise KeyError("engine '%s' does not exist" % name)
