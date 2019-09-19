def get_name_of_class(cls):
    if type(cls) != type:
        raise ValueError(str(cls) + 'is not type')
    return cls.__name__
