from icloud_api.engine import ICloudEngine
from argparse import ArgumentParser





def main(args):
    # Create a PyiCloudService object
    local_path = args.local_path
    icloud_path = args.icloud_path
    icloud_engine = ICloudEngine()
    icloud_engine.sync_paths(
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
        '--icloud_path',
        type=str
    )
    main(parser.parse_args())