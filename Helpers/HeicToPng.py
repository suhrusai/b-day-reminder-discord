from wand.image import Image


def heic_to_png(heic_file):
    heic_file_name = heic_file
    output_png_name = heic_file_name.replace('.heic', '.png')

    with Image(filename=heic_file) as img:
        img.format = 'png'
        img.save(filename=output_png_name)

    return output_png_name
# Usage example
