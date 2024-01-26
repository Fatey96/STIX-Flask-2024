from stix2 import Bundle



def create_bundle(stix_objects, relationships):
    """
    Creates a STIX bundle from given STIX objects and relationships.

    :param stix_objects: A list of STIX objects.
    :param relationships: A list of STIX relationship objects.
    :return: A STIX Bundle object.
    """
    all_objects = stix_objects + relationships
    return Bundle(objects=all_objects).serialize(pretty=True)
