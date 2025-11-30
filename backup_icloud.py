from pyicloud import PyiCloudService
import os
import json
import getpass

username = input("Enter your iCloud username: ")
password = getpass.getpass("Enter your iCloud password: ")
api = PyiCloudService(secrets["username"], secrets["password"])
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


top_dict =  api.drive['Uk_citizenship']
found_files = {}

def download_files(
    top_dict,
    local_path="",
    download=False
):
    for item in top_dict.dir():
        file_or_folder = top_dict[item]
        name = file_or_folder.name
        f_type = file_or_folder.type
        print(
            f"Found item: {name} of type {f_type}"
        )
        if f_type == 'file':
            found_files[os.path.join(local_path,name)]=file_or_folder
            # download = file_or_folder.open(stream=True)
            # with open(
            #     os.path.join(
            #         download_path,
            #         os.path.join(local_path,name)
            #     ),
            #     "wb"
            # ) as opened_file:
            #     # print(f"Downloading file to {os.path.join(local_path,name)}") 
            #     opened_file.write(download.raw.read())
            #     print(f"Downloaded file to {os.path.join(local_path,name)}")
        elif f_type == 'folder':
            # os.makedirs(
            #     os.path.join(
            #         download_path,
            #         os.path.join(local_path,name)
            #     ),
            #     exist_ok=True
            # )
            download_files(
                file_or_folder,
                local_path=os.path.join(local_path,name),
            )
    return found_files


if __name__ == "__main__":

    print(f"drive contents: {api.drive['Uk_citizenship']}")
    all_files = download_files(top_dict)
    breakpoint()
    print(f"All found files: {all_files}")