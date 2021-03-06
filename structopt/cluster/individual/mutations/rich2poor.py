import random
import numpy as np

from structopt.common.crossmodule import NeighborList


def rich2poor(atoms, surf_CN=11):
    '''Moves an atom from a rich region to a poor region'''

    syms = np.asarray(atoms.get_chemical_symbols())
    NN_list = NeighborList(atoms)
    NNs = [list(syms[i]) for i in NN_list]
    max_CN = max([len(NN) for NN in NNs])

    # Pick an atom in a rich environment
    ns = np.array([NNs[i].count(sym) for i, sym in enumerate(syms)])

    unique_ns = np.array(list(set(ns)))
    prob_rich = 2.0 ** unique_ns
    prob_rich /= np.sum(prob_rich)
    n = np.random.choice(unique_ns, p=prob_rich)
    indices_rich = np.where(ns == n)[0]
    index_rich = np.random.choice(indices_rich)
    symbol_rich = syms[index_rich]

    # Pick another atom in a poor environment
    indices_other = [i for i, sym in enumerate(syms) if sym != symbol_rich]
    ns_to_rich = np.array([max_CN - NNs[i].count(symbol_rich) for i in indices_other])
    unique_ns = np.array(list(set(ns_to_rich)))
    prob_poor = 2.0 ** unique_ns
    prob_poor /= np.sum(prob_poor)
    n_to_rich = np.random.choice(unique_ns, p=prob_poor)
    indices_poor = np.where(ns_to_rich == n_to_rich)[0]
    index_poor = np.random.choice(indices_poor)
    index_poor = indices_other[index_poor]
    symbol_poor = syms[index_poor]

    atoms[index_poor].symbol = symbol_rich
    atoms[index_rich].symbol = symbol_poor

    return
