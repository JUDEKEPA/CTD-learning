from io import StringIO
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from datetime import datetime
from collections import namedtuple
import os
from pycalphad.io.tdb import read_tdb
from pycalphad.variables import Species
from pycalphad.core.cache import fhash
from pycalphad.core.utils import recursive_tuplify
import matplotlib.pyplot as plt
from pycalphad import binplot
import pycalphad.variables as v

# --------------------------------------------
class Phase(object):    # pylint: disable=R0903
    """
    Phase in the database.

    Attributes
    ----------
    name : string
        System-local name of the phase.
    constituents : tuple of frozenset
        Possible sublattice constituents (elements and/or species).
    sublattices : list
        Site ratios of sublattices.
    model_hints : dict
        Structured "hints" for a Model trying to read this phase.
        Hints for major constituents and typedefs (Thermo-Calc) go here.
    """
    def __init__(self):
        self.name = None
        self.constituents = None
        self.sublattices = []
        self.model_hints = {}

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Phase({0!r})'.format(self.__dict__)

    def __hash__(self):
        return hash((self.name, self.constituents, tuple(self.sublattices),
                     tuple(sorted(recursive_tuplify(self.model_hints.items())))))

DatabaseFormat = namedtuple('DatabaseFormat', ['read', 'write'])
format_registry = {}


# I suppose that only .tdb file will be uploaded.
class Database: #pylint: disable=R0902
    """
    Structured thermodynamic and/or kinetic data.

    Attributes
    ----------
    elements : set
        Set of elements in database.
    species : set
        Set of species in database.
    phases : dict
        Phase objects indexed by their system-local name.
    symbols : dict
        SymEngine objects indexed by their name (FUNCTIONs in Thermo-Calc).
    references : dict
        Reference objects indexed by their system-local identifier.

    Examples
    --------
    >>> mydb = Database('crfeni_mie.tdb')
    """
    def __init__(self, tdb_file):
        self.tdb_file = tdb_file
        try:
            fd = open(tdb_file, mode='r')
        except (AttributeError, TypeError):
            # fname isn't actually a path, so we don't know the correct format
            raise ValueError('Please use valid tdb file')

        self.elements = set()
        self.species = set()
        self.phases = {}
        self.refstates = {}
        self._structure_dict = {}  # System-local phase names to global IDs
        self._parameters = TinyDB(storage=MemoryStorage)
        self._parameter_queue = []
        self.symbols = {}
        self.references = {}

        read_tdb(self, fd)

    def add_structure_entry(self, local_name, global_name):
        """
        Define a relation between the system-local name of a phase and a
        "global" identifier. This is used to link crystallographically
        similar phases known by different colloquial names.

        Parameters
        ----------
        local_name : string
            System-local name of the phase.
        global_name : object
            Abstract representation of symbol, e.g., in SymEngine format.

        Examples
        --------
        None yet.
        """
        self._structure_dict[local_name] = global_name

    def add_parameter(
        self, param_type, phase_name, constituent_array, param_order, param, ref=None,
        diffusing_species=None, force_insert=True, **kwargs,
        ):
        """
        Add a parameter.

        Parameters
        ----------
        param_type : str
            Type name of the parameter, e.g., G, L, BMAGN.
        phase_name : str
            Name of the phase.
        constituent_array : list
            Configuration of the sublattices (elements and/or species).
        param_order : int
            Polynomial order of the parameter.
        param : object
            Abstract representation of the parameter, e.g., in SymEngine format.
        ref : str, optional
            Reference for the parameter.
        diffusing_species : str, optional
            (If kinetic parameter) Diffusing species for this parameter.
        force_insert : bool, optional
            If True, inserts into the database immediately. False is a delayed insert (for performance).
        kwargs : Any
            Additional metadata to insert into the parameter dictionary

        Examples
        --------
        None yet.
        """
        species_dict = {s.name: s for s in self.species}
        new_parameter = {
            'phase_name': phase_name,
            'constituent_array': tuple(tuple(species_dict.get(s.upper(), Species(s)) for s in xs) for xs in constituent_array),  # must be hashable type
            'parameter_type': param_type,
            'parameter_order': param_order,
            'parameter': param,
            'diffusing_species': Species(diffusing_species),
            'reference': ref
        }
        new_parameter.update(kwargs)
        if force_insert:
            self._parameters.insert(new_parameter)
        else:
            self._parameter_queue.append(new_parameter)

    def add_phase(self, phase_name, model_hints, sublattices):
        """
        Add a phase.

        Parameters
        ----------
        phase_name : string
            System-local name of the phase.
        model_hints : dict
            Structured "hints" for a Model trying to read this phase.
            Hints for major constituents and typedefs (Thermo-Calc) go here.
        sublattices : list
            Site ratios of sublattices.

        Examples
        --------
        None yet.
        """
        new_phase = Phase()
        new_phase.name = phase_name
        # Need to convert from ParseResults or else equality testing will break
        new_phase.sublattices = tuple(sublattices)
        new_phase.model_hints = model_hints
        self.phases[phase_name] = new_phase

    def add_phase_constituents(self, phase_name, constituents):
        """
        Add a phase.

        Parameters
        ----------
        phase_name : string
            System-local name of the phase.
        constituents : list
            Possible phase constituents (elements and/or species).

        Examples
        --------
        None yet.
        """
        species_dict = {s.name: s for s in self.species}
        try:
            # Need to convert constituents from ParseResults
            # Otherwise equality testing will be broken
            self.phases[phase_name].constituents = tuple([frozenset([species_dict[s.upper()] for s in xs]) for xs in constituents])
        except KeyError:
            print("Undefined phase "+phase_name)
            raise
    def search(self, query):
        """
        Search for parameters matching the specified query.

        Parameters
        ----------
        query : object
            Structured database query in TinyDB format.

        Examples
        --------
        >>>> from tinydb import where
        >>>> db = Database()
        >>>> eid = db.add_parameter(...) #TODO
        >>>> db.search(where('eid') == eid)
        """
        return self._parameters.search(query)

    def process_parameter_queue(self):
        """
        Process the queue of parameters so they are added to the TinyDB in one transaction.
        This avoids repeated (expensive) calls to insert().
        """
        result = self._parameters.insert_multiple(self._parameter_queue)
        self._parameter_queue = []
        return result


db_alzn = Database('..//alzn_mey.tdb') #'alzn_mey.tdb'

my_phases_alzn = ['LIQUID', 'FCC_A1', 'HCP_A3']

# Create a matplotlib Figure object and get the active Axes
fig = plt.figure(figsize=(9,6))
axes = fig.gca()

# Compute the phase diagram and plot it on the existing axes using the `plot_kwargs={'ax': axes}` keyword argument
binplot(db_alzn, ['AL', 'ZN', 'VA'] , my_phases_alzn, {v.X('ZN'):(0,1,0.02), v.T: (300, 1000, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})

plt.show()

#db_test = Database()