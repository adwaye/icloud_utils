from pyicloud import PyiCloudService
from pyicloud.services.drive import DriveNode
import logging,os,sys
import glob
from pathlib import Path

logging.getLogger().setLevel(logging.INFO)

def get_path_object(
    api: PyiCloudService,
    path: str,
):
    """Get a path object from iCloud Drive given a path string."""
    path_parts = [part for part in path.split('/') if part]
    current_dict = api.drive

    for part in path_parts:
        if part in current_dict.dir():
            current_dict = current_dict[part]
        else:
            raise FileNotFoundError(f"Path '{path}' not found in iCloud Drive.")

    return current_dict


def download_file(
    icloud_file: DriveNode,
    local_path: str,
):
    """Download a file from iCloud Drive to a local path."""
    
    if icloud_file.type != 'file':
        logging.error(
            f"The provided icloud_file is not a file: {icloud_file.name}"
        )
        return 0
    name = icloud_file.name
    if not local_path.endswith(name):
        local_path = os.path.join(local_path, name)


    download = icloud_file.open(stream=True)
    try:
        with open(local_path,"wb") as opened_file:
            logging.debug(f"Downloading file to {local_path}") 
            opened_file.write(download.raw.read())
            logging.info(f"Downloaded file to {local_path}")
    except Exception as e:
        logging.error(f"Error downloading file to {local_path}: {e}")
    finally:
        download.close()
    



def authenticate(username: str, password: str) -> PyiCloudService:
    """Authenticate to iCloud and return the PyiCloudService instance."""
    api = PyiCloudService(username, password)

    if api.requires_2fa:
        security_key_names = api.security_key_names

        if security_key_names:
            print(
                f"Security key confirmation is required. "
                f"Please plug in one of the following keys: {', '.join(security_key_names)}"
            )

            devices = api.fido2_devices

            print("Available FIDO2 devices:")

            for idx, dev in enumerate(devices, start=1):
                print(f"{idx}: {dev}")

            choice = click.prompt(
                "Select a FIDO2 device by number",
                type=click.IntRange(1, len(devices)),
                default=1,
            )
            selected_device = devices[choice - 1]

            print("Please confirm the action using the security key")

            api.confirm_security_key(selected_device)

        else:
            print("Two-factor authentication required.")
            code = input(
                "Enter the code you received of one of your approved devices: "
            )
            result = api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print(
                    "Failed to request trust. You will likely be prompted for confirmation again in the coming weeks"
                )

    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print(
                "  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber')))
            )

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)
    return api


def find_all_files_remote(
    top_dir:DriveNode,
    local_path="",
    found_files={}
)-> dict:
    """Recursively find all files in the given iCloud Drive directory.
    
    Parameters
    ----------
    top_dir:  pyicloud.services.drive.DriveNode
        The top-level iCloud Drive directory to search.
    local_path: 
        The local path prefix for found files.

    Returns
    -------
    dict
        Returns a dictionary mapping local file paths to iCloud Drive file 
        objects relative to the top_dir. The keys are the paths relative to
        local_path and the values are the corresponding DriveNode objects.
    """
    for item in top_dir.dir():
        file_or_folder = top_dir[item]
        name = file_or_folder.name
        f_type = file_or_folder.type
        print(
            f"Found item: {name} of type {f_type}"
        )
        if f_type == 'file':
            found_files[os.path.join(local_path,name)]=file_or_folder
        elif f_type == 'folder':
            find_all_files_remote(
                top_dir=file_or_folder,
                local_path=os.path.join(local_path,name),
                found_files=found_files
            )
    return found_files


def find_all_files_local(
    top_dir: str,
):
    """Finds all files in the local directory

    Parameters
    ----------
    top_dir : str | Path
        Location where all files need to be found
    """
    all_files =[]
    top_dir = os.path.join(top_dir,'**')
    for file in glob.iglob(top_dir, recursive=True):
        if os.path.isfile(file):
            all_files.append(file)
    return all_files


def make_upload_path(
    file_path: str,
    icloud_path: str,
    local_path: str|Path,
):
    """Makes the upload path for icloud

    For example, if the icloud_path is set to be path/to/icloud
    and the local_file_path is <path>/<to>/<top_dir>
    while the file path is <path>/<to>/<top_dir>/<file_path>
    then the output should be path/to/icloud/<file_path>
    
    Parameters
    ----------
    file_path: str
        The full local file path which needs to be converted to an icloud file path
    icloud_path: str
        The icloud path where the file needs to be uploaded
    local_path: str
       The local path where the file is located, the icloud file path is created
       relative to this one

    returns
    -------
    str
        The full path to the file on icloud, relative to the local path
    """
    relative_path = file_path.split(local_path)[1]
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    icloud_path= os.path.join(icloud_path, relative_path)
    return icloud_path



if __name__=="__main__":
    top_dir = '/media/adwaye/Backup/tax_return'

    found_files = find_all_files_local(top_dir)
    print(found_files)
    found_file = found_files[0]
    icloud_path = 'Tax'
    print(found_file)
    upload_path = make_upload_path(found_file, icloud_path, top_dir)

