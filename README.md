# audio-converter
A tool for converting files in an audio library

Usage:

```cmd
python3 main.py -rd <directory with audio files> -o <where to put the converted files>
```

Options:

```
-d, --directory  path to the directory where the files are located
-r, --recursive  if provided, the tool will recursively walk each subdirectory contained within the path specified with the directory option
-o, --out-dir    Specifies the root dir of where to store the output. The directory structure from the input will be maintained in the output
```
