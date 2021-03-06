""" defines the filesystem model
"""
import os
import glob
import types
import shutil
import itertools
import autofile.io_


class DataFile():
    """ file manager for a given datatype """

    def __init__(self, name, writer_=(lambda _: _), reader_=(lambda _: _)):
        """
        :param name: the file name
        :type name: str
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        :param removable: Is this file removable?
        :type removable: bool
        """
        self.name = name
        self.writer_ = writer_
        self.reader_ = reader_
        self.removable = False

    def path(self, dir_pth):
        """ file path
        """
        return os.path.join(dir_pth, self.name)

    def exists(self, dir_pth):
        """ does this file exist?
        """
        pth = self.path(dir_pth)
        return os.path.isfile(pth)

    def write(self, val, dir_pth):
        """ write data to this file
        """
        assert os.path.exists(dir_pth), (
            'No path exists: {}'.format(dir_pth)
        )
        pth = self.path(dir_pth)
        val_str = self.writer_(val)
        autofile.io_.write_file(pth, val_str)

    def read(self, dir_pth):
        """ read data from this file
        """
        assert self.exists(dir_pth), (
            'Either requested file {} or requested path does not exist {}'.format(self, dir_pth)
        )

        pth = self.path(dir_pth)
        val_str = autofile.io_.read_file(pth)
        val = self.reader_(val_str)
        return val

    def remove(self, dir_pth):
        """ remove this file

        (only possible if `removable` attribute is set to `True`)
        """
        if self.removable:
            pth = self.path(dir_pth)
            os.remove(pth)
        else:
            raise ValueError("This data series is not removable")

    def __repr__(self):
        """ represent this object as a string
        """
        return "DataFile('{}')".format(self.name)


class DataSeries():
    """ directory manager mapping locator values to a directory series
    """

    def __init__(self, prefix, map_, nlocs, depth, loc_dfile=None,
                 root_ds=None, removable=False):
        """
        :param map_: maps `nlocs` locators to a segment path consisting of
            `depth` directories
        :param info_map_: maps `nlocs` locators to an information object, to
            be written in the data directory
        """
        assert os.path.isdir(prefix), (
            'Path is not a dir: {}'. format(prefix)
        )
        self.prefix = os.path.abspath(prefix)
        self.map_ = map_
        self.nlocs = nlocs
        self.depth = depth
        self.loc_dfile = loc_dfile
        self.root = root_ds
        self.removable = removable
        self.file = types.SimpleNamespace()
        self.JSON = 'db.json'
        self.json = types.SimpleNamespace()

    def add_data_files(self, dfile_dct):
        """ add DataFiles to the DataSeries
        """
        dfile_dct = {} if dfile_dct is None else dfile_dct

        for name, dfile in dfile_dct.items():
            assert isinstance(name, str)
            assert isinstance(dfile, DataFile)
            dsfile = DataSeriesFile(ds=self, dfile=dfile)
            setattr(self.file, name, dsfile)

    def path(self, locs=()):
        """ absolute directory path
        """
        if self.root is None:
            prefix = self.prefix
        else:
            root_locs = self._root_locators(locs)
            locs = self._self_locators(locs)
            prefix = self.root.path(root_locs)
        assert len(locs) == self.nlocs

        pth = self.map_(locs)
        assert _path_is_relative(pth)
        assert _path_has_depth(pth, self.depth)
        return os.path.join(prefix, pth)

    def exists(self, locs=()):
        """ does this directory exist?
        """
        pth = self.path(locs)
        return os.path.isdir(pth)

    def remove(self, locs=()):
        """ remove this directory

        (only possible if `removable` attribute is set to `True`)
        """
        if self.removable:
            pth = self.path(locs)
            if self.exists(locs):
                shutil.rmtree(pth)
        else:
            raise ValueError("This data series is not removable")

    def create(self, locs=()):
        """ create a directory at this prefix
        """
        # recursively create starting from the first root directory
        if self.root is not None:
            root_locs = self._root_locators(locs)
            self.root.create(root_locs)

        # create this directory in the chain, if it doesn't already exist
        if not self.exists(locs):
            pth = self.path(locs)
            os.makedirs(pth)

            if self.loc_dfile is not None:
                locs = self._self_locators(locs)
                self.loc_dfile.write(locs, pth)

    def existing(self, root_locs=(), relative=False):
        """ return the list of locators for existing paths
        """
        if self.nlocs == 0:
            # If there are no locators, this DataSeries only produces one
            # directory and we can just check if it exists or not
            if self.exists():
                locs_lst = ([],)
            else:
                locs_lst = ()
        else:
            # If there are one or more locators, we need to read in from the
            # locator data files
            assert self.nlocs > 0

            if self.loc_dfile is None:
                raise ValueError("This function does not work "
                                 "without a locator DataFile")

            root_nlocs = self.root_locator_count()

            # Recursion for when we have a root DataSeries
            if len(root_locs) < root_nlocs:
                locs_lst = tuple(itertools.chain(*(
                    self.existing(root_locs_)
                    for root_locs_ in self.root.existing(root_locs))))
            else:
                assert root_nlocs == len(root_locs), (
                    '{} != {}'.format(root_nlocs, len(root_locs))
                )
                pths = self._existing_paths(root_locs)
                locs_lst = tuple(self.loc_dfile.read(pth) for pth in pths
                                 if self.loc_dfile.exists(pth))
                if not relative:
                    locs_lst = tuple(map(list(root_locs).__add__, locs_lst))

        return locs_lst

    def _existing_paths(self, root_locs=()):
        """ existing paths at this prefix/root directory
        """
        if self.root is None:
            prefix = self.prefix
        else:
            prefix = self.root.path(root_locs)

        pth_pattern = os.path.join(prefix, *('*' * self.depth))
        pths = filter(os.path.isdir, glob.glob(pth_pattern))
        pths = tuple(sorted(os.path.join(prefix, pth) for pth in pths))
        return pths
        
    def json_path(self, json_layer=None):
        """ json file path
        """
        if self.root is None:
            prefix = self.prefix
        else:
            prefix = self.root.path()
        if json_layer:
            prefix = self._remove_layer_from_path(prefix, json_layer)
        return os.path.join(prefix, self.JSON)

    def json_exists(self, json_layer=None):
        """ does this file exist?
        """
        pth = self.json_path(json_layer=json_layer)
        return os.path.isfile(pth)

    def json_existing(self, locs=(), json_layer=None):
        """ returns a list of locations (aka keys) in the json file
        """
        locs = []
        if self.json_exists(json_layer=json_layer):
            json_data = autofile.json_.read_json(self.json_path(json_layer=json_layer))
            keys = json_data.keys()
            dct = json_data
            for nested_key in locs:
                if nested_key in keys:
                    dct = dct[nested_key]
                    keys = dct.keys()
                else:
                    dct = {}
                    keys = []
            locs = []
            for key in keys:
                if isinstance(dct[key], dict):
                    locs.append(key)
            locs = tuple([key] for key in keys)
            
        return locs

    def _map(self, locs):
        """ returns a list of mapped locations
        """
        if locs:
            locs = [self.map_(locs)]
        return locs

    def add_json_entries(self, entry_dct):
        """ add DataFiles to the DataSeries
        """
        entry_dct = {} if entry_dct is None else entry_dct

        for name, obj in entry_dct.items():
            assert isinstance(name, str)
            assert isinstance(obj, JSONObject)
            jsentry = JSONEntry(js=self, jobject=obj)
            setattr(self.json, name, jsentry)

    def json_create(self, json_layer=None):
        """ json file creation
        """
        if not self.json_exists():
            autofile.json_.write_json(
                {}, self.json_path(json_layer=json_layer))

    def _remove_layer_from_path(self, path, json_layer):
        head, tail = os.path.split(path)
        if tail == json_layer:
            path = head
        return path

    def root_locator_count(self):
        """ count the number of root locator values recursively
        """
        if self.root is None:
            root_nlocs = 0
        else:
            root_nlocs = self.root.nlocs + self.root.root_locator_count()
        return root_nlocs

    # helpers
    def _self_locators(self, locs):
        """ locators for this DataSeriesDir
        """
        nlocs = len(locs)
        assert nlocs >= self.nlocs
        root_nlocs = nlocs - self.nlocs
        return locs[root_nlocs:]

    def _root_locators(self, locs):
        """ locators for the root DataSeriesDir, if there is one
        """
        nlocs = len(locs)
        assert nlocs >= self.nlocs
        root_nlocs = nlocs - self.nlocs
        return locs[:root_nlocs]

    def __repr__(self):
        """ represent this object as a string
        """
        return "DataSeries('{}', {})".format(self.prefix, self.map_.__name__)


class DataSeriesFile():
    """ file manager mapping locator values to files in a directory series
    """

    def __init__(self, ds, dfile):
        self.dir = ds
        self.file = dfile
        self.removable = False

    def path(self, locs=()):
        """ absolute file path
        """
        return self.file.path(self.dir.path(locs))

    def exists(self, locs=()):
        """ does this file exist?
        """
        return self.file.exists(self.dir.path(locs))

    def write(self, val, locs=()):
        """ write data to this file
        """
        self.file.write(val, self.dir.path(locs))

    def read(self, locs=()):
        """ read data from this file
        """
        return self.file.read(self.dir.path(locs))

    def remove(self, locs=()):
        """ remove this file

        (only possible if `removable` attribute is set to `True`)
        """
        if self.removable:
            pth = self.path(locs)
            os.remove(pth)
        else:
            raise ValueError("This data series is not removable")

    def __repr__(self):
        """ represent this object as a string
        """
        return ("DataSeriesFile('{}', {}, '{}')"
                .format(self.dir.prefix, self.dir.map_.__name__,
                        self.file.name))


class JSONObject():
    def __init__(self, name, json_prefix=(None, None), function=None, writer_=(lambda _: _), reader_=(lambda _: _)):
        """
        :param name: the file name
        :type name: str
        :param writer_: writes data to a string
        :type writer_: callable[object->str]
        :param reader_: reads data from a string
        :type reader_: callable[str->object]
        :param removable: Is this file removable?
        :type removable: bool
        """
        self.name = name
        self.json_prefix, self.json_layer = json_prefix
        self.removable = False
        self.writer_ = writer_
        self.reader_ = reader_
   
    def items(self, path):
        """ what are the parent keys in this json file
        """
        keys = []
        entries = []
        if os.path.isfile(path):
           keys, entries = zip(*self.read_json(path).items())
        return keys, entries

    def _add_layer(self, key):
        layered_key = key
        if self.json_layer:
            layered_key = self.json_prefix.copy()
            layered_key.append(self.json_layer)
            layered_key.extend(key)
        return layered_key

    def keys(self, path):
        keys, _ = self.items(path)
        return keys

    def entries(self, path):
        _, entries = self.items(path)
        return entries 

    def read_json(self, path):
        return autofile.json_.read_json(path)

    def write_json(self, json_data, path):
        autofile.json_.write_json(json_data, path)

    def exists(self, key, path):
        exists = True
        key = self._add_layer(key)
        json_data = self.read_json(path)
        keys = json_data.keys()
        dct = json_data
        for nested_key in key:
            if nested_key in keys:
                dct = dct[nested_key]
                keys = dct.keys()
            else:
                exists = False
        if exists:
            if self.name not in dct:
                exists = False
        return exists

    def read(self, key, path):
        json_data = self.read_json(path)
        return self._read(key, json_data)

    def _read(self, key, json_data):
        exists = True
        key = self._add_layer(key)
        keys = json_data.keys()
        dct = json_data
        for nested_key in key:
            if nested_key in keys:
                dct = dct[nested_key]
                keys = dct.keys()
            else:
                exists = False
        if exists:
            if self.name in dct:
                return self.reader_(dct[self.name] )

    def read_all(self, keys, path):
        json_data = self.read_json(path)
        ret = []
        for key in keys:
            ret.append(self._read(key, json_data)) 
        return ret    

    def write(self, val, key, path):
        key = self._add_layer(key)
        current_json = self.read_json(path)
        keys = current_json.keys()
        dct = current_json
        for nested_key in key:
            if nested_key not in keys:
                dct[nested_key] = {}
            dct = dct[nested_key]
            keys = dct.keys()
        val = self.writer_(val)    
        dct[self.name] = val 
        self.write_json(current_json, path)

    def write_all(self, vals, all_keys, path):
        current_json = self.read_json(path)
        for key, val in zip(all_keys, vals):
            key = self._add_layer(key)
            keys = current_json.keys()
            dct = current_json
            for nested_key in key:
                if nested_key not in keys:
                    dct[nested_key] = {}
                dct = dct[nested_key]
                keys = dct.keys()
            val = self.writer_(val)    
            dct[self.name] = val 
        self.write_json(current_json, path)

class JSONEntry():
    def __init__(self, js, jobject):
        """ json manager mapping locator values to objects in a json file
        """
        self.js = js
        self.json = jobject
        self.removable = False

    def exists(self, key=('database_entry'), mapping=True):
        """ does this entry exist?
        """
        ret = False
        if mapping:
            ret = self.json.exists(self.js._map(key), self.js.json_path(
                json_layer=self.json.json_layer))
        else:
            ret = self.json.exists(key, self.js.json_path(
                json_layer=self.json.json_layer))
        return ret    
    
    def existing(self, key=()):
        """ returns the keys nested under this key 
        """
        return self.js.json_existing(locs=self.json._add_layer(key),
                                     json_layer=self.json.json_layer)

    def write(self, val, key=('database_entry'), mapping=True):
        """ write data to this file
        """
        if not self.js.json_exists(json_layer=self.json.json_layer):
            self.js.json_create(json_layer=self.json.json_layer)
        if mapping:
            key = self.js._map(key)
        self.json.write(val, key, self.js.json_path(
            json_layer=self.json.json_layer))

    def write_all(self, vals, keys=(('database_entry')), mapping=True):
        """ write data to this file
        """
        if not self.js.json_exists(json_layer=self.json.json_layer):
            self.js.json_create(json_layer=self.json.json_layer)
        if mapping:
            new_keys = []
            for key in keys:
               new_keys.append(self.js._map(key))
        else:
            new_keys = keys
        self.json.write_all(vals, new_keys, self.js.json_path(
            json_layer=self.json.json_layer))

    def read(self, key=('database_entry'), mapping=True):
        """ read data from this file
        """
        ret = None
        if self.exists(key, mapping=mapping):
            if mapping:
                ret = self.json.read(self.js._map(key), self.js.json_path(
                    json_layer=self.json.json_layer))
            else:
                ret = self.json.read(key, self.js.json_path(
                    json_layer=self.json.json_layer))
        return ret       

    def read_all(self, keys=(('database_entry')), mapping=True):
        """ read data from this file
        """
        ret = []
        new_keys = []
        for key in keys:
            if self.exists(key, mapping=mapping):
                if mapping:
                    new_keys.append(self.js._map(key))
                else:
                    new_keys.append(key)
        if new_keys:            
            ret = self.json.read_all(new_keys, self.js.json_path(
                json_layer=self.json.json_layer))
        return ret       


def _path_is_relative(pth):
    """ is this a relative path?
    """
    return os.path.relpath(pth) == pth


def _path_has_depth(pth, depth):
    """ does this path have the given depth?
    """
    return len(_os_path_split_all(pth)) == depth


def _os_path_split_all(pth):
    """ grabbed this from the internet """
    allparts = []
    while 1:
        parts = os.path.split(pth)
        if parts[0] == pth:    # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        if parts[1] == pth:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        pth = parts[0]
        allparts.insert(0, parts[1])
    return allparts
