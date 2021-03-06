import logging
import sys
import os

from structopt.tools.dictionaryobject import DictionaryObject
sys.modules['gparameters'] = DictionaryObject({})

from structopt.io.parameters import read as read_parameters
from structopt.io.parameters import write as write_parameters
from structopt.io.logger_utils import initialize_logger, initialize_logger_for_root
from structopt import common


def setup(parameter_file):
    # Read in the parameters
    parameters = read_parameters(parameter_file)
    sys.modules['gparameters'].update(parameters)

    # Setup all the loggers
    logging_level = parameters.logging.get("logging_level", "info")
    logging_level = getattr(logging, logging_level.upper())

    rank = parameters.mpi.rank
    path = parameters.logging.path
    os.makedirs(path, exist_ok=True)

    logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'output.log'), name="output", level=logging_level)
    logger_by_rank = initialize_logger(filename=os.path.join(path, 'output-by-rank-{}.log'.format(rank)), name="by-rank", level=logging_level)

    default_logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'default.log'), name="default", level=logging_level)

    fitness_logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'fitnesses.log'), name="fitness", level=logging_level)

    genealogy_logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'genealogy.log'), name="genealogy", level=logging_level)

    timing_logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'timing.log'), name="timing", level=logging_level)

    if logging_level <= logging.DEBUG:
        debug_logger = initialize_logger_for_root(rank=rank, filename=os.path.join(path, 'debug.log'), name="debug", level=logging_level)
        debug_logger_by_rank = initialize_logger(filename=os.path.join(path, 'debug-by-rank-{}.log'.format(rank)), name="debug-by-rank", level=logging_level)

    write_parameters(parameters)
    return parameters

