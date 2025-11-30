
from icloud_api.utils import authenticate
from icloud_api.utils import (
    get_path_object, 
    download_file,
    find_all_files
)

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
        # self.sync_upwards(local_path)

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
            parent_folder = Path(key).parent
            # breakpoint()
            if not parent_folder.exists():
                parent_folder.mkdir(parents=True,exist_ok=True)
            download_file(
                val,
                local_path=key
            )

    @staticmethod
    def sync_upwards(local_path: str)->None:
        """Upload all files from local path to iCloud."""
        # TODO: find all files in local directory
        # TODO: find overlap with downloaded files
        # upload files that are in local but now in downloaded
        local_files = Path().rglob(Path(local_path))
        raise NotImplementedError(
            'Not yet implemented, can only do downward syncs'
        )
        
        


            
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
    