import mimetypes
from pathlib import Path

from wand.image import Image

BASE_DIR = Path('.')

SOURCE_FOLDER = BASE_DIR / 'source'
THUMBNAILS_FOLDER = BASE_DIR / 'thumbnails'

MAX_HEIGHT = 135
MAX_WIDTH = 240


def generate_thumbnail(filename: str):
    print(f'➡️ Generating thumbnail for {filename} ⬅️')
    source_file_path = SOURCE_FOLDER / filename
    thumbnail_file_path = THUMBNAILS_FOLDER / filename

    content_type, _ = mimetypes.guess_type(filename)

    # Reference:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    if content_type in [
        'image/jpeg',
        'image/png',
        'image/tiff',
        'image/webp',
    ]:
        # Resize the image using ImageMagick.
        with Image(filename=source_file_path) as image:
            height = image.height
            width = image.width
            print(f'Original image: {source_file_path}')
            print(f'Original image size: {width}x{height}')

            # Clone the image in order to process
            with image.clone() as thumbnail:
                # if larger than MAX_WIDTH x MAX_HEIGHT,
                # fit within box, preserving aspect ratio
                thumbnail.transform(resize=f'{MAX_WIDTH}x{MAX_HEIGHT}>')

                # Save the image
                thumbnail.save(filename=thumbnail_file_path)

                print(f'✅ Thumbnail saved in {thumbnail_file_path}')
    else:
        print(f'🚫 Content type "{content_type}" is not supported')


if __name__ == '__main__':
    for file in SOURCE_FOLDER.iterdir():
        generate_thumbnail(filename=file.name)
