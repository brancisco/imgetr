import sys
import os
import re
import argparse
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from math import floor

VALID_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'bmp', 'tiff', 'webp', 'heif', 'pdf']
DOWNLOAD_BAR_LENGTH = 20

def main():
    parser = argparse.ArgumentParser(description='Download images from a website.')
    parser.add_argument('website_url', metavar='website', type=str,
        help='the website to download images from')
    parser.add_argument('-o', '--output_dir', type=str, nargs='?', default='.', const='.',
        help='the directory to download the files into')
    parser.add_argument('-c', '--class_list', type=str, nargs='+', metavar='class', default=[],
        help='list of css classes the images on the page contains')
    parser.add_argument('-t', '--tag', type=str, nargs='*', metavar='tag', default=['img'],
        help='list of html tags where images are contained')
    parser.add_argument('-q', '--query_key', type=str, nargs='?', metavar='query_key',
        help='query parameter key in an img src that contains image filename')
    parser.add_argument('-u', '--unknown_img_ext', type=str, nargs='?', metavar='.ext', default='.jpg', const='.jpg',
        help='name of ext for images with no ext')
    parser.add_argument('-r', '--rename', type=str, nargs='?', metavar='regex',
        help='regex pattern selecting groups of the output image filename to be concat together')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='print out the name of each file downloaded')
    args = parser.parse_args()

    N_TERMINAL_COLUMNS = os.get_terminal_size().columns

    try:
        response = requests.get(args.website_url)
    except Exception as e:
        print(e.args[0])
        sys.exit(1)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []
    for tag in args.tag:
        images += soup.select('.'.join([tag] + args.class_list))

    unknown_img_name_count = 1
    n_imgs = len(images)
    padding = len(str(n_imgs + 1))
    qkey = args.query_key

    if n_imgs < 1:
        print(f'No images found on page {args.website_url}.')
        exit(0)

    for i, img in zip(range(len(images)), images):
        url = img.get('src')
        if not url: continue
        url_parsed = urlparse(url)
        query = parse_qs(url_parsed.query)
        string_to_match = query[qkey][0] if qkey and qkey in query else url_parsed.path
        match = re.search(r'([^/]+)(\.%s)$' % '|'.join(VALID_EXTS), string_to_match)
        fname = None
        if match:
            fname = match.group()
        else:
            fname = str(unknown_img_name_count).zfill(padding) + args.unknown_img_ext
            unknown_img_name_count += 1
        try:
            imgbytes = requests.get(url).content
        except Exception as e:
            print(f'[x] {type(e).__name__} : {url}'.ljust(N_TERMINAL_COLUMNS))
            continue

        outname = fname
        if args.rename:
            try:
                outmatch = re.search(args.rename, fname)
            except Exception as e:
                print(f'Regex {args.rename} failed: {type(e).__name__} {e.args}'.ljust(N_TERMINAL_COLUMNS))
                outmatch = None
            if outmatch:
                outname = ''.join(outmatch.groups())

        with open(os.path.join(args.output_dir, outname), 'wb') as fout:
            fout.write(imgbytes)
            percent_complete = i / n_imgs
            n_bars = floor(percent_complete * DOWNLOAD_BAR_LENGTH)
            download_bar = '[%s]' % ('='*n_bars).ljust(DOWNLOAD_BAR_LENGTH, '*')
            if args.verbose:
                print(('[\N{CHECK MARK}] %s' % outname).ljust(N_TERMINAL_COLUMNS))
                outname = ''
            print(('%s %.1f%% %s ...' % (download_bar, percent_complete * 100, outname)).ljust(N_TERMINAL_COLUMNS), end='\r')
    
    print(('[%s] 100%% Complete.' % ('='*DOWNLOAD_BAR_LENGTH)).ljust(N_TERMINAL_COLUMNS))

if __name__ == '__main__':
    main()