# Usage
Set of utils for syncing icloud with a local folder

```bash
#!/bin/bash
uv run python backup_icloud.py --local_path <target_local_path> --icloud_path <source_folder_on_icloud>
```

Currently, the library only supports downward syncs. Upload syncs will be supported soon!

This is based off of the [pyicloud](https://github.com/picklepete/pyicloud) library.
Credits to [picklepete](https://github.com/picklepete) for the awesome work on this!

TODO:
- add upload syncs
- add more error handling
- add tests