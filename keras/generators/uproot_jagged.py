from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import uproot

def make_generator(paths, batch_size, max_cluster_size):
    def get_event():
        for data in uproot.iterate(paths, 'events', ['n', 'x', 'y']):
            n = data['n']
            x = data['x']
            y = data['y']

            start = 0
            end = batch_size
            while True:
                if end > n.shape[0]:
                    this_batch_size = n.shape[0] - start
                else:
                    this_batch_size = batch_size

                ntotal = np.sum(n[start:end])
                nfeat = x.content.shape[1]

                v_x = np.zeros((this_batch_size, max_cluster_size, nfeat), dtype=np.float)

                batch_indices = np.repeat(np.arange(this_batch_size), n[start:end])

                cluster_indices = np.r_[tuple(np.s_[:x] for x in n[start:end])]

                v_x[batch_indices, cluster_indices] = x[start:end].flatten()

                yield [v_x, n[start:end]], y[start:end]

                if end >= n.shape[0]:
                    break

                start = end
                end += batch_size

    return get_event


if __name__ == '__main__':
    generator = make_generator('/tmp/yiiyama/test_0.root', 2, 256)()

    print(next(generator))
