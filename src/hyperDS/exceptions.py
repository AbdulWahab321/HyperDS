class InvalidDataType(Exception):
    pass
class InvalidSyntax(Exception):
    pass
def invalidDataType(data_type):
    raise InvalidDataType("Invalid data type: %s" % data_type + " expected string, integer, float, dict, tuple, list, boolean, NoneType")
def syntax_error(details):
    raise InvalidSyntax(details)