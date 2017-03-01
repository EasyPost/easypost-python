import pkg_resources


VERSION = pkg_resources.resource_stream('easypost', '../VERSION').read().decode('utf-8').strip()
