import pkg_resources

def getResourcePath(resource):
    return pkg_resources.resource_filename('resources', resource)
