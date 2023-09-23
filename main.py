import argparse
import sys

import h5py
import numpy as np


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


def read_h5(filename=None, dataset=None):
    """Yield h5 dataset."""
    with h5py.File(filename, "r") as file:
        obj = file if dataset is None else file[dataset]
        yield from np.array(obj)


def read_h5_recursive(file, dataset):
    """Yield h5 dataset names recursively."""
    obj = file if dataset is None else file[dataset]

    if isinstance(obj, h5py.Group):
        for ds in obj:
            next_dataset = ds if dataset is None else dataset + "/" + ds
            yield from read_h5_recursive(file, next_dataset)

    elif isinstance(obj, h5py.Dataset):
        yield obj.name


def alternate_generators(*generators):
    """Yield alternating generator."""
    generator_list = [iter(g) for g in generators]

    while True:
        try:
            for g in generator_list:
                yield next(g)
        except StopIteration:
            break

    for g in generator_list:
        yield from g


def zip_generators(*generators):
    """Yield zipped generator."""
    generator_list = [iter(g) for g in generators]

    while True:
        try:
            yield [next(g) for g in generator_list]
        except StopIteration:
            break


def main():
    parser = argparse.ArgumentParser(
        prog="H5 File Tool",
        description="Cli tool to parse H5 file.",
    )
    parser.add_argument("filename")
    parser.add_argument("dataset", nargs="*")
    parser.add_argument("-d", "--delimiter", default=";")
    parser.add_argument("-r", "--recursive", action="store_true")
    args = parser.parse_args()

    if args.recursive:
        with h5py.File(args.filename, "r") as file:
            print(*read_h5_recursive(file, None), sep="\n")
        return

    if not args.dataset:
        args.dataset = [None]
    objs_generators = [read_h5(args.filename, ds) for ds in args.dataset]
    zipped_generators = zip_generators(*objs_generators)
    print(
        *[args.delimiter.join(list(map(str, elems))) for elems in zipped_generators],
        sep="\n"
    )


if __name__ == "__main__":
    try:
        main()
    except BaseException as err:
        eprint(err)
