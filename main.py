import argparse
import os
import sys
import threading

from audio import convert_to_mp3, get_audio_format_from_filename
from fs import convert_filename_to_mp3, extract_audio_files, walk_directory_tree

parser = argparse.ArgumentParser(
    prog="AudioTools",
    description="A home made tool to perform various operations on an audio library"
)

parser.add_argument("-d", "--directory", type=str, required=True, help="path to the directory where the files are located")
parser.add_argument("-r", "--recursive", action="store_true", required=False, help="if provided, the tool will recursively walk each subdirectory contained within the path specified with the directory option")
parser.add_argument("-o", "--out-dir", type=str, required=True, help="Specifies the root dir of where to store the output. The directory structure from the input will be maintained in the output")

args = parser.parse_args()

dirname = args.directory
out_dir = args.out_dir

if not os.path.isdir(dirname):
    sys.stderr.write(f"Directory '{dirname}' does not exist")
    sys.exit(1)

all_files = extract_audio_files(walk_directory_tree(dirname))

threads = []
print("Processing files...")
for file, i in zip(all_files, range(len(all_files))):
    output_file = convert_filename_to_mp3(file.replace(dirname, out_dir))
    t = threading.Thread(
        target=convert_to_mp3,
        args=(
            file,
            convert_filename_to_mp3(output_file),
            get_audio_format_from_filename(file)
        )
    )
    t.start()
    threads.append(t)

[t.join() for t in threads]
print("Done")