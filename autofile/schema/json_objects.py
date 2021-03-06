""" JsonFiles
"""
from autofile import model
import autofile.data_types


def input_file(file_prefix, json_prefix=(None, None)):
    """ generate input entry in json file
    """
    name = autofile.data_types.name.input_file(file_prefix)
    return model.JSONObject(name=name, json_prefix=json_prefix)


def output_file(file_prefix):
    """ generate output entry in json file
    """
    name = autofile.data_types.name.output_file(file_prefix)
    return model.JSONObject(name=name)


def energy(file_prefix, json_prefix=(None, None)):
    """ generate energy  entry in json file
    """
    name = autofile.data_types.name.energy(file_prefix)
    return model.JSONObject(name=name, json_prefix=json_prefix)


def geometry(file_prefix):
    """ generate geometry entry in json file
    """
    name = autofile.data_types.name.geometry(file_prefix)
    return model.JSONObject(name=name)


def information(file_prefix, function=None, json_prefix=(None, None)):
    """ information DataFile

    :param function: optional information-generator function, for checking the
        function signature against the information object
    :type function: callable
    """
    def writer_(inf_obj):
        if function is not None:
            assert autofile.info.matches_function_signature(inf_obj, function)
        inf_str = autofile.data_types.swrite.information(inf_obj)
        return inf_str

    def reader_(inf_str):
        inf_obj = autofile.data_types.sread.information(inf_str)
        if function is not None:
            assert autofile.info.matches_function_signature(inf_obj, function)
        return inf_obj

    name = autofile.data_types.name.information(file_prefix)
    return model.JSONObject(name=name, json_prefix=json_prefix,
                          writer_=writer_, reader_=reader_)


def locator(file_prefix, map_dct_, loc_keys):
    """ locator DataFile

    Specifiers are stored in information files according to `map_dct_` and read
    back out according to `loc_keys_`. The file may contain auxiliary
    information (such as SMILES along with InChI), but for the read to work it
    must contain each locator value.

    :param map_dct_: Maps on the locator list to the values stored in the
        information file, by key.
    :type map_dct_: dict[key: callable]
    :param loc_keys: Keys to the original locator values.
    :type loc_keys: tuple[str]
    """
    name = autofile.data_types.name.information(file_prefix)
    return model.JSONObject(name=name) 

def gradient(file_prefix):
    """ generate gradient DataFile
    """
    name = autofile.data_types.name.gradient(file_prefix)
    writer_ = autofile.data_types.swrite.gradient_array
    reader_ = autofile.data_types.sread.gradient_array
    return model.JSONObject(writer_=writer_,reader_=reader_,name=name) 


def hessian(file_prefix):
    """ generate hessian DataFile
    """
    name = autofile.data_types.name.hessian(file_prefix)
    return model.JSONObject(name=name) 


def harmonic_frequencies(file_prefix):
    """ generate harmonic_frequencies DataFile
    """
    name = autofile.data_types.name.harmonic_frequencies(file_prefix)
    return model.JSONObject(name=name) 


def anharmonic_frequencies(file_prefix):
    """ generate anharmonic_frequencies DataFile
    """
    name = autofile.data_types.name.anharmonic_frequencies(file_prefix)
    return model.JSONObject(name=name) 


def anharmonic_zpve(file_prefix):
    """ generate anharmonic_zpve DataFile
    """
    name = autofile.data_types.name.anharmonic_zpve(file_prefix)
    return model.JSONObject(name=name) 


def anharmonicity_matrix(file_prefix):
    """ generate anharmonicity matrix DataFile
    """
    name = autofile.data_types.name.anharmonicity_matrix(file_prefix)
    return model.JSONObject(name=name) 


def vibro_rot_alpha_matrix(file_prefix):
    """ generate vibro_rot_alpha matrix DataFile
    """
    name = autofile.data_types.name.vibro_rot_alpha_matrix(file_prefix)
    return model.JSONObject(name=name) 


def quartic_centrifugal_dist_consts(file_prefix):
    """ generate vibro_rot_alpha matrix DataFile
    """
    name = (
        autofile.data_types.name.quartic_centrifugal_dist_consts(file_prefix))
    return model.JSONObject(name=name) 


def zmatrix(file_prefix):
    """ generate zmatrix DataFile
    """
    name = autofile.data_types.name.zmatrix(file_prefix)
    return model.JSONObject(name=name) 


def vmatrix(file_prefix):
    """ generate vmatrix DataFile
    """
    name = autofile.data_types.name.vmatrix(file_prefix)
    return model.JSONObject(name=name) 


def trajectory(file_prefix):
    """ generate trajectory DataFile
    """
    name = autofile.data_types.name.trajectory(file_prefix)
    return model.JSONObject(name=name) 


def graph(file_prefix):
    """ generate graph DataFile
    """
    name = autofile.data_types.name.graph(file_prefix)
    return model.JSONObject(name=name) 


def transformation(file_prefix):
    """ generate transformation DataFile
    """
    name = autofile.data_types.name.transformation(file_prefix)
    return model.JSONObject(name=name) 


def lennard_jones_epsilon(file_prefix):
    """ generate lennard_jones_epsilon DataFile
    """
    name = autofile.data_types.name.lennard_jones_epsilon(file_prefix)
    return model.JSONObject(name=name) 


def lennard_jones_sigma(file_prefix):
    """ generate lennard_jones_sigma DataFile
    """
    name = autofile.data_types.name.lennard_jones_sigma(file_prefix)
    return model.JSONObject(name=name) 


# helpers
def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError
