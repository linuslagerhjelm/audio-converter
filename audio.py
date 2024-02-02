import io
import os
from pydub import AudioSegment
from pydub.utils import mediainfo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.aiff import AIFF
from mutagen.wave import WAVE
from PIL import Image

from fs import create_dir_for_file

class InvalidFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def convert_to_mp3(input: str, output: str, format: str):
    """
    Converts the provided file from the specified format to mp3 and saves it 
    to the path specified by output. This function stores the output to disc
    and thus does not return anything.

    Note: output needs to include .mp3

    Args:
        input (str): path to the input file
        output (str): where to save the output
        format (str): format of the input file, currently supports .aiff and .wav

    """
    audio = AudioSegment.from_file(input, format=format)
    metadata = mediainfo(input)
    create_dir_for_file(output)
    audio.export(output, format="mp3", bitrate="320k", tags=metadata["TAG"])
    cover, mime = get_cover_image(input, format)
    mp3_audio = MP3(output, ID3=ID3)
    mp3_audio.tags.add(
        APIC(
            encoding = 3,
            mime=mime,
            type = 3,
            desc = "Cover",
            data = cover,
        )
    )
    mp3_audio.save()

def get_audio_format_from_filename(file: str):
    """
    Extracts the format from the file name of the specified file

    Args:
        file (str): The file to get format from
    
    Returns:
        str: The format
    """
    return file.split(".")[-1]

def get_cover_image(input: str, format: str):
    """
    Extracts the cover image from a supported file

    Args:
        file (str): The file to extract cover image from

    Returns:
        (bytes, str): A tuple containing the image bytes and the mime type of the image
    """
    if format == "aiff":
        return get_cover_image_from_aiff(input)
    
    if format == "wav":
        return get_cover_image_from_wav(input)
    
    raise InvalidFormatError(f"Unknown format '{format}'")


def get_cover_image_from_aiff(file: str):
    """
    Extracts the cover image from an aiff file

    Args:
        file (str): The aiff file to extract cover image from

    Returns:
        (bytes, str): A tuple containing the image bytes and the mime type of the image
    """
    audio = AIFF(file)
    img_tag_data = audio["APIC:cover"] if "APIC:cover" in audio else audio["APIC:"]
    mime = img_tag_data.mime
    extension = "jpg" if mime == "image/jpeg" else "png"
    image = Image.open(io.BytesIO(img_tag_data.data))
    temp_img_filename = f"{file}_tmpimg.{extension}"
    image.save(temp_img_filename)
    img_bytes = open(temp_img_filename, 'rb').read()
    os.remove(temp_img_filename)
    return (img_bytes, mime)

def get_cover_image_from_wav(file: str):
    """
    Extracts the cover image from an wav file

    Args:
        file (str): The wav file to extract cover image from

    Returns:
        (bytes, str): A tuple containing the image bytes and the mime type of the image
    """
    audio = WAVE(file)
    mime = audio["APIC:"].mime
    extension = "jpg" if mime == "image/jpeg" else "png"
    image = Image.open(io.BytesIO(audio['APIC:'].data))
    temp_img_filename = f"{file}_tmpimg.{extension}"
    image.save(temp_img_filename)
    img_bytes = open(temp_img_filename, 'rb').read()
    os.remove(temp_img_filename)
    return (img_bytes, mime)
