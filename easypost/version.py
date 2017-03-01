import pkg_resources


VERSION = pkg_resources.resource_stream('easypost', '../VERSION').read().strip()
