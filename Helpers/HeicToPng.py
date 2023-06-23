import pyheif
from PIL import Image


def heic_to_png(heic_file):
    heic_file_name = heic_file
    heif_file = pyheif.read(heic_file)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    output_png_name = heic_file_name.replace('.heic', '.png')
    image.save(output_png_name, "PNG")
    return output_png_name
# Usage example
