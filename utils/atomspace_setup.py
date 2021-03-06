__author__ = "Enku Wendwosen & Abdulrahman Semrie"

import logging
from opencog.atomspace import AtomSpace
from opencog.scheme_wrapper import scheme_eval_h
import config

logger = logging.getLogger("annotation-service")


def load_atomspace():
    """
    loads atomspace with knowledge bases and annotation scheme functions found in scm directory.
    :return: atomspace instance
    """
    atomspace = AtomSpace()
    logger.info("Loading Atoms")
    scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.OPENCOG_DEPS_PATH))
    atomspace = load_functions(atomspace)
    atomspace = load_datasets(atomspace)
    logger.info("Atoms loaded!")
    return atomspace


def load_datasets(atomspace):
    """
    loads datasets from scm/datasets directory to atomspace
    :param atomspace: atomspace instance that will be loaded with datasets.
    :return: a loaded atomspace instance
    """
    logger.info("Loading datasets")
    if config.PRODUCTION_MODE:
        logger.info("In Production Mode")
        for dataset in config.DATASET_PATHs:
            scheme_eval_h(atomspace, '(primitive-load "{}")'.format(dataset))

        return atomspace
    else:
        logger.info("In Dev Mode")
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(config.TEST_DATASET))
        return atomspace


def load_functions(atomspace):
    """
    loads annotation functions from scm/functions directory to atomspace
    :param atomspace: atomspace instance taht will be loaded with functions
    :return: a loaded atomspace instance
    """
    logger.info("loading functions")
    for fn in config.FUNCTION_PATHs:
        scheme_eval_h(atomspace, '(primitive-load "{}")'.format(fn))

    return atomspace
