import h5py
import pathlib


class RecursiveFileIterator:

    def __init__(self, file):
        self.file = file
        self.pointer = ""

    def __iter__(self):
        if self.lchild is not None:
            yield from self.lchild
        yield self
        if self.rchild is not None:
            yield from self.rchild



def recursive_h5(file_path: pathlib.Path) -> list[tuple[str, int, bool]]:
    """Iterate recursively through file."""
    item_list = []
    with h5py.File(file_path, "r") as file:
        for i, (name, obj) in enumerate(file.items()):
            is_last = i == len(file) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, 0, is_last))
                for e in recursive_group(file_path, f"{name}", 1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", 0, is_last))

    return item_list


def recursive_group(
    file_path: pathlib.Path, group: str, depth: int
) -> list[tuple[str, int, bool]]:
    """Iterate recursively through group."""
    item_list = []
    with h5py.File(file_path, "r") as file:
        for i, (name, obj) in enumerate(file[group].items()):
            is_last = i == len(file[group]) - 1
            if str(type(obj)) == "<class 'h5py._hl.group.Group'>":
                item_list.append((name, depth, is_last))
                for e in recursive_group(file_path, f"{group}/{name}", depth + 1):
                    item_list.append(e)

            elif str(type(obj)) == "<class 'h5py._hl.dataset.Dataset'>":
                item_list.append((f"{name}", depth, is_last))

    return item_list
