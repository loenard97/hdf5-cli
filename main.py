import h5py
import argparse
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


class RecursiveFileIterator:

    def __init__(self, file: h5py.File):
        self.file = file
        self.pointer = "/"

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.file.filename}, {self.pointer}>"

    def recursive_h5(self) -> list[str]:
        """Iterate recursively through file."""
        item_list = []
        for name, obj in self.file.items():
            if isinstance(obj, h5py.Group):
                item_list.append(name)
                for e in self.recursive_group(f"{name}"):
                    item_list.append(e)

            elif isinstance(obj, h5py.Dataset):
                item_list.append(f"{name}")

        return item_list

    def recursive_group(self, group: str) -> list[str]:
        """Iterate recursively through group."""
        item_list = []
        for name, obj in self.file[group].items():
            if isinstance(obj, h5py.Group):
                item_list.append(f"{group}/{name}")

                for e in self.recursive_group(f"{group}/{name}"):
                    item_list.append(e)

            elif isinstance(obj, h5py.Dataset):
                item_list.append(f"{group}/{name}")

        return item_list

    def __iter__(self):
        for name in self.recursive_h5():
            yield name


def main():
    parser = argparse.ArgumentParser(
        prog="hdf5-cli",
        description="HDF5 file cli tool",
    )
    parser.add_argument("filename", nargs="?")
    parser.add_argument("dataset", nargs="?")
    parser.add_argument("-l", "--list", action="store_true", default=True)
    parser.add_argument("-r", "--recursive", action="store_true")

    args = parser.parse_args()
    if not args.filename:
        eprint("No file given")

    with h5py.File(args.filename, "r") as file:
        if args.dataset is not None:
            obj = file[args.dataset]
            if isinstance(obj, h5py.Group) or isinstance(obj, h5py.Dataset):
                print(*obj, sep="\n")
            else:
                eprint("Type Error")

        elif args.list and args.recursive:
            print(*RecursiveFileIterator(file), sep="\n")

        elif args.list:
            print(*file, sep="\n")

        else:
            eprint("Unknown arguments")


if __name__ == '__main__':
    try:
        main()
    except BaseException as err:
        eprint(err)
