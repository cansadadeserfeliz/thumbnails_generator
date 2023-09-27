import mimetypes
from pathlib import Path

from wand.image import Image
import fitz  # imports the pymupdf library

BASE_DIR = Path('.')

FILES_SOURCE_FOLDER = BASE_DIR / 'source' / 'files'
PDFS_SOURCE_FOLDER = BASE_DIR / 'source' / 'pdfs'
THUMBNAILS_FOLDER = BASE_DIR / 'thumbnails'
PDF_IMAGES_FOLDER = BASE_DIR / 'pdf_images'

# Use 2x of the thumbnail size to avoid image pixelation
MAX_HEIGHT = 135 * 2
MAX_WIDTH = 240 * 2


def generate_thumbnail(filename: str):
    print(f'➡️ Generating thumbnail for {filename} ⬅️')
    source_file_path = FILES_SOURCE_FOLDER / filename
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


def pdf_to_images(filename: str):
    source_file_path = PDFS_SOURCE_FOLDER / filename
    with fitz.open(open(source_file_path, 'rb')) as pdf:
        for idx, page in enumerate(pdf, start=1):
            pix = page.get_pixmap()
            the_page_bytes = pix.pil_tobytes(format='JPEG')
            with open(PDF_IMAGES_FOLDER / f'{idx}.jpeg', "wb") as outf:
                outf.write(the_page_bytes)


if __name__ == '__main__':
    # Generate thumbnails
    for file in FILES_SOURCE_FOLDER.iterdir():
        generate_thumbnail(filename=file.name)

    print('-' * 80)

    # Convert PDF to images
    pdf_filename = 'sample_pdf_10_pages.pdf'
    pdf_to_images(filename=pdf_filename)

    pdf_filename = 'password-protected-sample-123456.pdf'
    pdf_to_images(filename=pdf_filename)

    pdf_filename = 'corrupt_file.pdf'
