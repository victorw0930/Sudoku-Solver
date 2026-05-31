import logging
import sys
import argparse

import solver


def test_func(x: int) -> int:
    return x

# Intentionally passing a string instead of an int
test_func("Hello World")
