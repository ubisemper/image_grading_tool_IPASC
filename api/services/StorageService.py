from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def __init__(self, credentials):
        pass

    @abstractmethod
    def get_all_file_names(self):
        pass

    @abstractmethod
    def get_all_folder_names(self):
        pass

    @abstractmethod
    def get_file_names_in_folder(self, folder_name):
        pass

    @abstractmethod
    def get_file_by_name(self):
        pass

    @abstractmethod
    def upload_file(self, file):
        pass
