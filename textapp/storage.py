from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """Ίδιο όνομα αρχείου -> αντικατάσταση"""

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name