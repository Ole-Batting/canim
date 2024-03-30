# Canim
Code animation library.
Currently only supporting python highlighting (yaml also works fine).

This library uses poetry for package management.
```commandline
poetry install
```

Basic usage:
```commandline
poetry run python canim/typewriter.py --in-path path/to/folder_or_file
                                      --out-path path/to/output_folder
                                      [--lq]
                                      [--set-width SETWIDTH]
                                      [--tail TAIL]
```

Options:

- `--in-path path/to/folder_or_file` Define input path. 
Can be folder/directory in which case all files (exluding ones starting with `_`) will be animated.
If path is a file then only that file will be animated.
- `--out-path path/to/output_folder` Define output path.
- `--lq` flag to indicate low quality run. Meant for testing purposes. 
If set then `configs/prototype.yaml` will be used as config.
Otherwise `configs/production.yaml` is used as config.
- `--set-width SETWIDTH` Set how many characters wide a page may be.
Default is 88.
- `--tail TAIL` Set how many static frames to add to tail of animation.
Default is 0.
