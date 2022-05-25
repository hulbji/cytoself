import os.path
from os.path import join
import umap
from typing import Optional


class BaseAnalysis:
    """
    Base class for Analysis
    """

    def __init__(
        self,
        datamanager,
        trainer,
        homepath: Optional[str] = None,
        **kwargs,
    ):
        self.datamanager = datamanager
        self.trainer = trainer
        self.reducer = None
        self.savepath_dict = {
            'homepath': join(trainer.savepath_dict['homepath'], 'analysis') if homepath is None else homepath
        }
        self._init_savepath()

    def _init_savepath(self):
        folders = ['umap_figures', 'umap_data', 'feature_spectra_figures', 'feature_spectra_data']
        for f in folders:
            p = join(self.savepath_dict['homepath'], f)
            if not os.path.exists(p):
                os.makedirs(p)
            self.savepath_dict[f] = p

    def _fit_umap(self, data, n_neighbors=15, min_dist=0.1, metric='euclidean', verbose=True, **kwargs):
        self.reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, metric=metric, verbose=verbose, **kwargs)
        self.reducer.fit(data.reshape(data.shape[0], -1))

    def _transform_umap(self, data, n_neighbors=15, min_dist=0.1, metric='euclidean', verbose=True, **kwargs):
        if self.reducer is None:
            self._fit_umap(data, n_neighbors, min_dist, metric, verbose, **kwargs)
        return self.reducer.transform(data.reshape(data.shape[0], -1))
