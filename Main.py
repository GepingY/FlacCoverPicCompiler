import argparse
from mutagen.flac import FLAC, Picture
from PIL import Image
import os
import traceback

def embed_cover(flac_path, image_path):
    try:
        audio = FLAC(flac_path)
    except Exception as e:
        print(f"Error loading FLAC file {flac_path}: {e}")
        return


    try:
        with Image.open(image_path) as img:
            width, height = img.size
            format = img.format.lower()
            mime = {
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
            }.get(format, 'image/jpeg')

            with open(image_path, 'rb') as f:
                image_data = f.read()

            picture = Picture()
            picture.data = image_data
            picture.type = 3
            picture.mime = mime
            picture.desc = ''
            picture.width = width
            picture.height = height
            picture.depth = 0


            audio.clear_pictures()
            audio.add_picture(picture)

            audio.save()
            print(f"Successfully embedded cover into {flac_path}")
    except Exception as e:
        print(f"Error embedding cover into {flac_path}: {e}")
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Embed cover picture into FLAC files')
    parser.add_argument('flac_files', nargs='+', help='Path to the FLAC files')
    parser.add_argument('image_file', help='Path to the cover image file')
    args = parser.parse_args()

    if not os.path.exists(args.image_file):
        print(f"Image file not found: {args.image_file}")
        return

    for flac_file in args.flac_files:
        embed_cover(flac_file, args.image_file)

if __name__ == '__main__':
    main()
