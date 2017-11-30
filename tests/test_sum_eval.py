import os
import sys
import plac
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from sumeval.cli.sum_eval import entory_point


if __name__ == "__main__":
    entory_point()
