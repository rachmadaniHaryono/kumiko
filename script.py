#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
require:
click hydrus-api tqdm
"""
import configparser
import io
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

import click
import cv2
import hydrus
from tqdm import tqdm

from kumikolib import Kumiko


def show_panels(path, tmin=220, tmax=255):
    import matplotlib.image as mpimg
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    k = Kumiko()
    k.tmin = tmin
    k.tmax = tmax
    k_res = k.parse_images([path])
    fig, ax = plt.subplots(1)
    fig.set_figwidth(k_res[0]['size'][0]/fig.dpi)
    fig.set_figheight(k_res[0]['size'][1]/fig.dpi)
    # Display the image
    img = mpimg.imread(path)
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Create a Rectangle patch
    for item in k_res[0]['panels']:
        rect = patches.Rectangle(
            (item[0], item[1]), item[2], item[3],
            linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
    plt.axis('off')
    plt.show()


@click.command()
@click.argument('config-file')
@click.argument("paths", nargs=-1)
def process_hydrus(paths, config_file):
    if config_file:
        config = configparser.ConfigParser()
        with open(config_file) as f:
            config.read_file(f)
    else:
        print('config file required')
        return
    kwargs = {}
    for key in ['w_min_p', 'h_min_p', 'w_min', 'h_min']:
        value = config['main'].get(key, None)
        if value:
            kwargs[key] = float(value)
    if 'right_to_left' in config['main']:
        right_to_left = bool(int(config['main']['right_to_left']))
        k = Kumiko(options={'right_to_left': right_to_left})
    else:
        k = Kumiko()
    cl = hydrus.Client(config['main']['access_key'])
    for path in tqdm(paths):
        hash_ = Path(path).stem
        with NamedTemporaryFile() as f:
            tqdm.write('hash: {}'.format(hash_))
            resp = cl.get_file(hash_=hash_)
            f.write(resp.content)
            k_res = k.parse_image(f.name, **kwargs)
            img = cv2.imread(path)
            panels = k_res['panels']
            for panel in tqdm(panels):
                p = panel
                crop_img = img[p[1]:p[1]+p[3], p[0]:p[0]+p[2]]
                _, im_buf_arr = cv2.imencode(".jpg", crop_img)
                byte_im = im_buf_arr.tobytes()
                res = cl.add_file(io.BytesIO(byte_im))
                tqdm.write(str(res))
                time.sleep(0.5)


if __name__ == '__main__':
    process_hydrus()
