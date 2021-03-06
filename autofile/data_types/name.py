""" file namers
"""


class Extension():
    """ file extensions """
    INFORMATION = '.yaml'
    INPUT_LOG = '.inp'
    OUTPUT_LOG = '.out'
    PROJROT_LOG = '.prot'
    SHELL_SCRIPT = '.sh'
    ENERGY = '.ene'
    GEOMETRY = '.xyz'
    TRAJECTORY = '.t.xyz'
    ZMATRIX = '.zmat'
    VMATRIX = '.vmat'
    GRADIENT = '.grad'
    HESSIAN = '.hess'
    HARMONIC_ZPVE = '.hzpve'
    ANHARMONIC_ZPVE = '.azpve'
    HARMONIC_FREQUENCIES = '.hfrq'
    ANHARMONIC_FREQUENCIES = '.afrq'
    PROJECTED_FREQUENCIES = '.pfrq'
    ANHARMONICITY_MATRIX = '.xmat'
    VIBRO_ROT_MATRIX = '.vrmat'
    CENTRIF_DIST_CONSTS = '.qcd'
    LJ_EPSILON = '.eps'
    LJ_SIGMA = '.sig'
    EXTERNAL_SYMMETRY_FACTOR = '.esym'
    GRAPH = '.g.yaml'
    TRANSFORMATION = '.t.yaml'
    # Various VaReCoF files
    VRC_TST = '.tst'
    VRC_DIVSUR = '.divsur'
    VRC_MOLP = '.molpro'
    VRC_TML = '.tml'
    VRC_STRUCT = '.struct'
    VRC_POT = '.pot'
    VRC_FLUX = '.flux'
    JSON = '.json'


def information(file_name):
    """ adds information extension, if missing
    """
    return _add_extension(file_name, Extension.INFORMATION)


def input_file(file_name):
    """ adds input file extension, if missing
    """
    return _add_extension(file_name, Extension.INPUT_LOG)


def output_file(file_name):
    """ adds output file extension, if missing
    """
    return _add_extension(file_name, Extension.OUTPUT_LOG)


def projrot_file(file_name):
    """ adds projrot file extension, if missing
    """
    return _add_extension(file_name, Extension.PROJROT_LOG)


def run_script(file_name):
    """ adds run script extension, if missing
    """
    return _add_extension(file_name, Extension.SHELL_SCRIPT)


def energy(file_name):
    """ adds energy extension, if missing
    """
    return _add_extension(file_name, Extension.ENERGY)


def geometry(file_name):
    """ adds geometry extension, if missing
    """
    return _add_extension(file_name, Extension.GEOMETRY)


def trajectory(file_name):
    """ adds trajectory extension, if missing
    """
    return _add_extension(file_name, Extension.TRAJECTORY)


def zmatrix(file_name):
    """ adds zmatrix extension, if missing
    """
    return _add_extension(file_name, Extension.ZMATRIX)


def vmatrix(file_name):
    """ adds variable zmatrix extension, if missing
    """
    return _add_extension(file_name, Extension.VMATRIX)


def gradient(file_name):
    """ adds gradient extension, if missing
    """
    return _add_extension(file_name, Extension.GRADIENT)


def hessian(file_name):
    """ adds hessian extension, if missing
    """
    return _add_extension(file_name, Extension.HESSIAN)


def harmonic_zpve(file_name):
    """ adds harmonic zpve extension, if missing
    """
    return _add_extension(file_name, Extension.HARMONIC_ZPVE)


def anharmonic_zpve(file_name):
    """ adds anharmonic zpve extension, if missing
    """
    return _add_extension(file_name, Extension.ANHARMONIC_ZPVE)


def harmonic_frequencies(file_name):
    """ adds harmonic frequencies extension, if missing
    """
    return _add_extension(file_name, Extension.HARMONIC_FREQUENCIES)


def anharmonic_frequencies(file_name):
    """ adds anharmonic frequencies extension, if missing
    """
    return _add_extension(file_name, Extension.ANHARMONIC_FREQUENCIES)


def projected_frequencies(file_name):
    """ adds projected frequencies extension, if missing
    """
    return _add_extension(file_name, Extension.PROJECTED_FREQUENCIES)


def anharmonicity_matrix(file_name):
    """ adds anharmonicity maxtrix extension, if missing
    """
    return _add_extension(file_name, Extension.ANHARMONICITY_MATRIX)


def vibro_rot_alpha_matrix(file_name):
    """ adds vibro_rot_alpha maxtrix extension, if missing
    """
    return _add_extension(file_name, Extension.VIBRO_ROT_MATRIX)


def quartic_centrifugal_dist_consts(file_name):
    """ adds quartic centrifugal distortion constants, if missing
    """
    return _add_extension(file_name, Extension.CENTRIF_DIST_CONSTS)


def lennard_jones_epsilon(file_name):
    """ adds lennard-jones epsilon extension, if missing
    """
    return _add_extension(file_name, Extension.LJ_EPSILON)


def lennard_jones_sigma(file_name):
    """ adds lennard-jones sigma extension, if missing
    """
    return _add_extension(file_name, Extension.LJ_SIGMA)


def external_symmetry_factor(file_name):
    """ adds external symmetry number extension, if missing
    """
    return _add_extension(file_name, Extension.EXTERNAL_SYMMETRY_FACTOR)


def graph(file_name):
    """ adds graph extension, if missing
    """
    return _add_extension(file_name, Extension.GRAPH)


def transformation(file_name):
    """ adds transformation extension, if missing
    """
    return _add_extension(file_name, Extension.TRANSFORMATION)


def vrctst_tst(file_name):
    """ adds vrctst_tst extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_TST)


def vrctst_divsur(file_name):
    """ adds vrctst_divsur extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_DIVSUR)


def vrctst_molpro(file_name):
    """ adds vrctst_molpro extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_MOLP)


def vrctst_tml(file_name):
    """ adds vrctst_tml extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_TML)


def vrctst_struct(file_name):
    """ adds vrctst_struct extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_STRUCT)


def vrctst_pot(file_name):
    """ adds vrctst_pot extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_POT)


def vrctst_flux(file_name):
    """ adds vrctst_flux extension, if missing
    """
    return _add_extension(file_name, Extension.VRC_FLUX)


def _add_extension(file_name, ext):
    if not str(file_name).endswith(ext):
        file_name = '{}{}'.format(file_name, ext)
    return file_name
