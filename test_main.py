#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pathlib

from kumikolib import Kumiko


def test_parse_image():
    obj = Kumiko()
    img_path = str(pathlib.Path(__file__).parent / "doc" / "regular_expressions.png")
    res = obj.parse_image(img_path)
    with (pathlib.Path(__file__).parent / "xkcd.json").open() as f:
        exp_res = json.load(f)[0]
    assert res == exp_res
