class ShowAllDetailsMixin:
    """ Adds a get fields method to show all details in detail view"""
    def get_fields(self):
        return [
            (field.verbose_name, field.value_from_object(self))
            for field
            in self.__class__._meta.fields
        ]