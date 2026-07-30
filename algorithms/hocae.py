import numpy as np

class HO_CAE:
    def __init__(self, n, k, alpha):
        self.n = n
        self.k = k
        self.alpha = alpha

    def compute_threshold(self, magnitude_sq):
        if magnitude_sq.ndim == 2:
            # convert to 1d array by flattening
            magnitude_sq = magnitude_sq.flatten()

        # compute the order statistic for the given n and k
        p = 0
        est = []
        while p < len(magnitude_sq):
            est.append(np.average(magnitude_sq[p:p+self.n]))
            p += int(self.n//2)
    
        if len(est) != ((len(magnitude_sq) * 2) // self.n):
            raise ValueError(f"Expected {((len(magnitude_sq) * 2) // self.n)} estimates, got {len(est)}")
    
        est.sort(reverse=False)
        return est[self.k] * self.alpha