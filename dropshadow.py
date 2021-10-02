#!/usr/bin/env python3
from PIL import Image, ImageFilter, ImageOps
import sys
import argparse
from Xlib.display import Display

screen = Display(':0').screen()
WIDTH, HEIGHT = screen.width_in_pixels, screen.height_in_pixels

parser = argparse.ArgumentParser()
parser.add_argument("--background-blur", "-B", type=float, default=20.0, help="blur radius in pixels for background")
parser.add_argument("--shadow-blur", "-b", type=float, default=20.0, help="blur radius in pixels for shadow")
parser.add_argument("--width", "-W", type=int, default=WIDTH or 1920, help="width in pixels of output image")
parser.add_argument("--height", "-H", type=int, default=HEIGHT or 1080, help="height in pixels of output image")
parser.add_argument("--gap-size", "-g", type=int, default=200, help="minimum gap length in pixels from foreground to each edge")
parser.add_argument("--shadow-size", "-s", type=int, default=10, help="shadow length in pixels around each side of foreground")
parser.add_argument("--png", action="store_true", help="output as PNG instead of JPEG")
parser.add_argument('path', nargs='+')
args = parser.parse_args()

width_2, height_2 = args.width//2, args.height//2

for image_path in args.path:

  image=Image.open(image_path).convert('RGB')
  background = image.resize((args.width, args.height)).filter(ImageFilter.GaussianBlur(radius=args.background_blur)).convert('RGB')
  image.thumbnail(
                    ( min(args.width  - args.gap_size, image.width),
                      min(args.height - args.gap_size, image.height) ),
                    Image.ANTIALIAS
                 )

  shadow = Image.new('RGBA', (background.width, background.height), (0, 0, 0, 0))
  shadow_size2 = args.shadow_size * 2
  shadow_width, shadow_height = image.width+shadow_size2, image.height+shadow_size2
  shadow_width_2, shadow_height_2 = shadow_width//2, shadow_height//2
  shadow.paste(
    Image.new('RGBA', (shadow_width, shadow_height), (0,0,0,255)),
    ( (args.width-shadow_width)//2, (args.height-shadow_height)//2)
  )

  shadow = shadow.filter(ImageFilter.GaussianBlur(radius=30))

  background.paste(shadow, (0,0), shadow)  # third arg is the mask, PIL uses the alpha channel automatically

  background.paste(image, (width_2 - image.width//2, height_2 - image.height//2))

  # background.paste(
  #   0x44444488,
  #   [
  #     width_2 - shadow_width_2,   # left offset
  #     height_2 - shadow_height_2, # top offset
  #     width_2 + shadow_width_2,   # right offset
  #     height_2 + shadow_height_2, # bottom offset
  #   ]
  # )
  extension = "png" if args.png else "jpg"
  background.save(image_path.partition('.')[0] + '_dropshadow.' + extension)