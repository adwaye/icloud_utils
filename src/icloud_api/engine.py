from pyicloud import PyiCloudService
from icloud_api.utils import authenticate
from icloud_api.utils import (
    get_path_object, 
    download_file,
    find_all_files
)
import os
from pathlib import Path
import getpass


class ICloudEngine:
    def __init__(self, username: str | None=None, password: str |None=None):
        if username is None or password is None:
            if username is None:
                username = input("Enter your iCloud username: ")
            if password is None:
                password = getpass.getpass("Enter your iCloud password: ")
        self.api = authenticate(username,password)

    def sync_drive(self):
        pass

    # def sync_paths(self, icloud_file: str, local_path: str)->None:
    #     """Sync files between iCloud path and local path."""
    #     download = file_or_folder.open(stream=True)
    #     with open(
    #         os.path.join(
    #             download_path,
    #             os.path.join(local_path,name)
    #         ),
    #         "wb"
    #     ) as opened_file:
    #         # print(f"Downloading file to {os.path.join(local_path,name)}") 
    #         opened_file.write(download.raw.read())
    #         print(f"Downloaded file to {os.path.join(local_path,name)}")


    def sync_paths(self, icloud_path: str, local_path: str)->None:
        """Sync files between iCloud path and local path.
        
        Parameters
        ----------
        icloud_path : str
            The iCloud Drive path to sync.
        local_path : str
            The local filesystem path to sync.
        """
        icloud_object = get_path_object(self.api, icloud_path)
        all_files_remote = find_all_files(icloud_object,local_path)
        self.sync_downwards(all_files_remote)
        self.sync_upwards(local_path)

    @staticmethod
    def sync_downwards(all_files_remote: dict)->None:
        """Download all files from iCloud to local path.
        
        Parmameters
        ----------
        all_files : dict
            A dictionary of iCloud files to download. The keys are the local 
            paths, and the values are the iCloud file objects.
        """
        for key,val in all_files_remote.items():
            if not os.path.exists(key):
                os.makedirs(key, exist_ok=True)
            download_file(
                val,
                local_path=key
            )

    @staticmethod
    def sync_upwards(local_path: str)->None:
        """Upload all files from local path to iCloud."""
        
        local_files = Path().rglob(Path(local_path))
        breakpoint()
        # breakpoint()
        


            
if __name__ == "__main__":
    import json
    from icloud_api import get_project_root
    


    # icloud_engine = ICloudEngine(secrets["username"], secrets["password"])
    # icloud_engine = ICloudEngine()
    # all_files = find_all_files(top_dir =icloud_engine.api.drive['Uk_citizenship'])
    # icloud_engine.sync_upwards(
    local_path = "/home/adwaye/mnt_dir/immigration/naturalisation"
    local_files = Path(local_path).rglob('/*')
    breakpoint()
    