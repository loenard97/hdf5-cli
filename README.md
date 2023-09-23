<div align="center">

# HDF5 cli tool
A python based cli tool to view HDF5 files

![last commit](https://img.shields.io/github/last-commit/loenard97/hdf5-cli?&style=for-the-badge&logo=github&color=3776AB)
![repo size](https://img.shields.io/github/repo-size/loenard97/hdf5-cli?&style=for-the-badge&logo=github&color=3776AB)

</div>


HDF5 Files are developed by the [HDF Group](https://www.hdfgroup.org/solutions/hdf5/).
Each File can contain Groups that work similarly to folders and Datasets that represent raw data.
They are widely used in Industry and Academia to store large sets of raw data.


## 📋 Usage
Specify a file name to print all Groups and Datasets in that file.
The `-r` flag prints all Groups and Datasets recursively.
Append one or more Datasets to print their contents.

For example, to export Datasets to a csv file:

```python
$ python main.py data.h5 Data/x_data Data/y_data >out.csv
```
