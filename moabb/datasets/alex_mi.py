"""
Alex Motor imagery dataset.
"""

from .base import BaseDataset
from mne.io import Raw
import os

import moabb.datasets.download as dl

ALEX_URL = 'https://zenodo.org/record/806023/files/'

def data_path(subject, path=None, force_update=False, update_path=None,
              verbose=None):
    """Get path to local copy of ALEX dataset URL.

    Parameters
    ----------
    subject : int
        Number of subject to use
    path : None | str
        Location of where to look for the data storing location.
        If None, the environment variable or config parameter
        ``MNE_DATASETS_INRIA_PATH`` is used. If it doesn't exist, the
        "~/mne_data" directory is used. If the dataset
        is not found under the given path, the data
        will be automatically downloaded to the specified folder.
    force_update : bool
        Force update of the dataset even if a local copy exists.
    update_path : bool | None
        If True, set the MNE_DATASETS_INRIA_PATH in mne-python
        config to the given path. If None, the user is prompted.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see :func:`mne.verbose`).

    Returns
    -------
    path : list of str
        Local path to the given data file. This path is contained inside a list
        of length one, for compatibility.
    """  # noqa: E501
    if subject < 1 or subject > 8:
        raise ValueError("Valid subjects between 1 and 8, subject {:d} requested".format(subject))
    url = '{:s}subject{:d}.raw.fif'.format(ALEX_URL, subject)


    return dl.data_path(url, 'ALEXEEG', path, force_update, update_path, verbose)
    
class AlexMI(BaseDataset):
    """Alex Motor Imagery dataset"""

    def __init__(self, with_rest=False):
        self.subject_list = range(1, 9)
        self.name = 'Alex Motor Imagery'
        self.tmin = 0
        self.tmax = 3
        self.paradigm = 'Motor Imagery'
        self.event_id = dict(right_hand=2, feet=3)
        if with_rest:
            self.event_id['rest'] = 4

    def get_data(self, subjects):
        """return data for a list of subjects."""
        data = []
        for subject in subjects:
            data.append(self._get_single_subject_data(subject))
        return data

    def _get_single_subject_data(self, subject):
        """return data for a single subject"""
        raw = Raw(data_path(subject), preload=True)
        return [raw]