# UrbanWeb Digital — Local Images Pack

This package has been modified so **all image references are local** (assets/img/...).
Right now those files are **placeholders** so nothing breaks offline.

## To download the real images
1) Make sure you have Python 3 installed
2) Install requests:
   pip install requests
3) Run:
   python download_images.py

This will download the images listed in `assets/images.json` and overwrite the placeholders.

## Why this is needed
The original site referenced images on external CDNs (Unsplash). Those can break due to:
- network blocks
- CSP rules
- rate limits

Local images = stable.
