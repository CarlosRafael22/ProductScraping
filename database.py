class Database():

    def __init__(self):
        print('Initializing the database')

    @staticmethod
    def get_attribute_and_lookup_from_query_string(key_query_string: str) -> str:
        try:
            attribute, lookup = key_query_string.split('__')
        except ValueError:
            # print(excp)
            attribute = key_query_string.split('__')[0]
            lookup = None
        return (attribute, lookup)
    
    @staticmethod
    def filter_gte(attribute, value, list_to_filter):
            return list(filter(lambda x: (getattr(x, attribute, 0) or 0) >= value, list_to_filter))

    @staticmethod
    def filter_equals(attribute, value, list_to_filter):
        return list(filter(lambda x: getattr(x, attribute) == value, list_to_filter))
    
    @staticmethod
    def filter_lt(attribute, value, list_to_filter):
        return list(filter(lambda x: (getattr(x, attribute, 0) or 0) < value, list_to_filter))
    
    @staticmethod
    def filter_contains(attribute, value, list_to_filter):
        return list(filter(lambda x: value in (getattr(x, attribute, '') or ''), list_to_filter))

    @classmethod
    def filter(cls, objects, **kwargs):
        filtered_objects = objects
        for key, value in kwargs.items():
            # If we dont have the lookup on splitting then we handle it to not throw error
            (attribute, lookup) = Database.get_attribute_and_lookup_from_query_string(key)
            filter_function = {
                'gte': Database.filter_gte,
                'lt': Database.filter_lt,
                'contains': Database.filter_contains,
                None: Database.filter_equals
            }[lookup]
            filtered_objects = filter_function(attribute, value, filtered_objects)
        return filtered_objects