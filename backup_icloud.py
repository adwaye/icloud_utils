from pyicloud import PyiCloudService
from argparse import ArgumentParser

import getpass


username = input("Enter your iCloud username: ")
password = getpass.getpass("Enter your iCloud password: ")

def main(args):
    # Create a PyiCloudService object
    local_path = args.local_path
    icloud_path = args.icloud_path
    icloud_engine = PyiCloudService()
    icloud_engine.sync_path(
        icloud_path=icloud_path,
        local_path=local_path
    )


if __name__ == "__main__":
    parser = ArgumentParser(
        description='Program to download icloud folder locally',
    )
    parser.add_argument(
        '--local_path',
        type=str
    )
    parser.add_argument(
        '--icloud-path',
        type=str
    )
    main(parser.parse_args())