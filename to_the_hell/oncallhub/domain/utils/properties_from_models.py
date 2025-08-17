def make_property(attr):
    private_attr = f"_{attr}"

    def getter(self):
        return getattr(self, private_attr)

    def setter(self, value):
        setattr(self, private_attr, value)

    def deleter(self):
        delattr(self, private_attr)

    return property(getter, setter, deleter)
