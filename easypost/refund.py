from easypost.resource import (
    AllResource,
    CreateResource,
    NextPageResource,
)


class Refund(CreateResource, AllResource, NextPageResource):
    pass
