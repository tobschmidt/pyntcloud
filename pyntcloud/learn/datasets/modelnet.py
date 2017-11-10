from __future__ import print_function

import os
import urllib
import zipfile
from glob import glob
from shutil import rmtree
from .folder import ClassificationFolder

MODELNET_URLS = {
    10: "http://3dshapenets.cs.princeton.edu/ModelNet10.zip",
    40: "http://modelnet.cs.princeton.edu/ModelNet40.zip"
}


class ModelNet10(ClassificationFolder):

    def __init__(self,
                 root=None,
                 train=True,
                 transform=None,
                 target_transform=None,
                 load_3D_kwargs={"target_size": (32, 32, 32)}):

        if root is None:
            root = get_and_setup_modelnet(10)

        if train:
            root = "%s/train"%root
        else:
            root = "%s/test"%root

        super(ModelNet10, self).__init__(root, transform, target_transform, load_3D_kwargs)


class ModelNet40(ClassificationFolder):

    def __init__(self,
                 root=None,
                 train=True,
                 transform=None,
                 target_transform=None,
                 load_3D_kwargs={"target_size": (32, 32, 32)}):

        if root is None:
            root = get_and_setup_modelnet(40)

        if train:
            root = "%s/train"%root
        else:
            root = "%s/test"%root

        super(ModelNet40, self).__init__(root, transform, target_transform, load_3D_kwargs)


def get_and_setup_modelnet(N):
    """
    Download, Unzip, Rearange and Fix corrupted files of ModelNetN

    Parameters
    ----------
    N: 10 or 40

    Returns
    -------
    extract_folder: str
    """
    cwd = os.getcwd()
    zip_file = "%s/modelnet%i.zip"%(cwd, N)
    extract_folder = "%s/modelnet{N}"%(cwd, N)

    if not os.path.exists(zip_file):
        print("Downloading ModelNet%i"%N)
        urllib.request.urlretrieve(MODELNET_URLS[N], zip_file)

    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
        print("Unzipping ModelNet")
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall(extract_folder)

    print("Removing __MACOSX")
    # Thanks, Steve Jobs
    try:
        rmtree("%s/__MACOSX"%extract_folder)
    except IOError:
        pass

    print("Rearranging ModelNet")
    # create proper train/test split
    BASE = "%s/ModelNet%i/"%(extract_folder, N)
    for class_dir in os.listdir(BASE):
        if os.path.isdir(os.path.join(BASE, class_dir)):
            os.makedirs("%s/train/%s"%(extract_folder, class_dir))
            os.makedirs("%s/test/%s}"%(extract_folder, class_dir))

    # move to proper train/test split
    all_files = glob("%s/*/*/*.off"%(BASE))
    for src in all_files:
        class_dir = src.split("/")[-3]
        split = src.split("/")[-2]
        fname = src.split("/")[-1]
        dst = "%s/%s/%s/%s"%(extract_folder,split,class_dir,fname)
        os.rename(src, dst)

    print("Fixing wrong off files")
    all_files = glob("%s/*/*/*.off"%extract_folder)
    for path in all_files:
        f = open(path, 'r')
        lines = f.readlines()
        f.close()

        if lines[0].strip().lower() != 'off':

            splits = lines[0][3:].strip().split(' ')
            n_verts = int(splits[0])
            n_faces = int(splits[1])
            n_other = int(splits[2])

            f = open(path, 'w')
            f.write('OFF\n')
            f.write('%d %d %d\n' % (n_verts, n_faces, n_other))
            for line in lines[1:]:
                f.write(line)
            f.close()

    rmtree("%s"%BASE)

    return extract_folder
