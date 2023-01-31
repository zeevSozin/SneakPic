class Picture:
    def __init__(self, name, original_photo, processed_photo, meta):
        self.name = name
        self.original_photo = original_photo
        self.processed_photo = processed_photo
        self.metadata = meta
         
    def get_name(self):
        return self.name
         
    def set_name(self, name):
        self.name = name

    def get_Original_photo(self):
        return self.original_photo

    def set_Original_photo(self, photo):
        self.original_photo = photo

    def get_Processed_photo(self):
        return self.processed_photo

    def set_Processed_photo(self, photo):
        self.processed_photo = photo

    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

