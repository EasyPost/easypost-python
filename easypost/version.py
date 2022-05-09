VERSION = "7.1.1"

elements = VERSION.split("-")
numbers = [str(v) for v in elements[0].split(".")]
if len(elements) > 1:
    numbers.extend(elements[1])
numbers.extend(elements[1:])
VERSION_INFO = numbers
