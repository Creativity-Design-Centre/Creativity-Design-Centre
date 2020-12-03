from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from itertools import combinations, chain
import pyLDAvis
import math


class oBTM:
    """ Biterm Topic Model

        Code and naming is based on this paper http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.402.4032&rep=rep1&type=pdf
        Thanks to jcapde for providing the code on https://github.com/jcapde/Biterm
    """

    def __init__(self, num_topics, V, alpha=1., beta=0.01, l=0.5):
        self.K = num_topics
        self.V = V
        self.alpha = np.full(self.K, alpha)
        self.beta = np.full((len(self.V), self.K), beta)
        self.l = l

    def _gibbs(self, iterations):

        Z = np.zeros(len(self.B), dtype=np.int8)
        n_wz = np.zeros((len(self.V), self.K), dtype=int)
        n_z = np.zeros(self.K, dtype=int)

        for i, b_i in enumerate(self.B):
            topic = np.random.choice(self.K, 1)[0]
            n_wz[b_i[0], topic] += 1
            n_wz[b_i[1], topic] += 1
            n_z[topic] += 1
            Z[i] = topic

        for _ in range(iterations):
            for i, b_i in enumerate(self.B):
                n_wz[b_i[0], Z[i]] -= 1
                n_wz[b_i[1], Z[i]] -= 1
                n_z[Z[i]] -= 1
                P_w0z = (n_wz[b_i[0], :] + self.beta[b_i[0], :]
                         ) / (2 * n_z + self.beta.sum(axis=0))
                P_w1z = (n_wz[b_i[1], :] + self.beta[b_i[1], :]) / \
                    (2 * n_z + 1 + self.beta.sum(axis=0))
                P_z = (n_z + self.alpha) * P_w0z * P_w1z
                # P_z = (n_z + self.alpha) * ((n_wz[b_i[0], :] + self.beta[b_i[0], :]) * (n_wz[b_i[1], :] + self.beta[b_i[1], :]) /
                #                            (((n_wz + self.beta).sum(axis=0) + 1) * (n_wz + self.beta).sum(axis=0)))  # todo check out
                if P_z.sum() != 0:
                    P_z = P_z / P_z.sum()
                else:
                    P_z = P_z
                Z[i] = np.random.choice(self.K, 1, p=P_z)
                n_wz[b_i[0], Z[i]] += 1
                n_wz[b_i[1], Z[i]] += 1
                n_z[Z[i]] += 1

        return n_z, n_wz

    def fit_transform(self, B_d, iterations):
        self.fit(B_d, iterations)
        return self.transform(B_d)

    def fit(self, B_d, iterations):
        self.B = list(chain(*B_d))
        n_z, self.nwz = self._gibbs(iterations)

        self.phi_wz = (self.nwz + self.beta) / \
            np.array([(self.nwz + self.beta).sum(axis=0)] * len(self.V))
        self.theta_z = (n_z + self.alpha) / (n_z + self.alpha).sum()

        self.alpha += self.l * n_z
        self.beta += self.l * self.nwz

    def transform(self, B_d):

        P_zd = np.zeros([len(B_d), self.K])
        for i, d in enumerate(B_d):
            P_zb = np.zeros([len(d), self.K])
            for j, b in enumerate(d):
                P_zbi = self.theta_z * \
                    self.phi_wz[b[0], :] * self.phi_wz[b[1], :]
                P_zb[j] = P_zbi / P_zbi.sum()
            if P_zb.sum(axis=0).sum() != 0:
                P_zd[i] = P_zb.sum(axis=0) / P_zb.sum(axis=0).sum()
            else:
                P_zd[i] = P_zb.sum(axis=0)
        return P_zd


def vec_to_biterms(X):
    B_d = []
    for x in X:
        b_i = [b for b in combinations(np.nonzero(x)[0], 2)]
        B_d.append(b_i)
    return B_d


def topic_summuary(P_wz, X, V, M, verbose=True):
    res = {
        'coherence': [0] * len(P_wz),
        'top_words': [[None]] * len(P_wz)
    }
    for z, P_wzi in enumerate(P_wz):
        V_z = np.argsort(P_wzi)[:-(M + 1):-1]
        W_z = V[V_z]

        # calculate topic coherence score -> http://dirichlet.net/pdf/mimno11optimizing.pdf
        C_z = 0
        for m in range(1, M):
            for l in range(m):
                D_vmvl = np.in1d(np.nonzero(X[:, V_z[l]]), np.nonzero(
                    X[:, V_z[m]])).sum(dtype=int) + 1
                D_vl = np.count_nonzero(X[:, V_z[l]])
                if D_vl != 0:
                    C_z += math.log(D_vmvl / D_vl)

        res['coherence'][z] = C_z
        res['top_words'][z] = W_z
        if verbose:
            print('Topic {} | Coherence={:0.2f} | Top words= {}'.format(
                z, C_z, ' '.join(W_z)))
    return res


def transform(dataset, n_features=1000):
    vectorizer = TfidfVectorizer(
        max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer


new_list = []
with open('../product-reviewB07H625JJL-one_star.txt',  'r') as f:
    content = f.readlines()
    all_comment = 0
    positive_comment = 0
    for i in content:
        if i != '\n':
            all_comment += 1
            if(len(i) > 10):
                new_list.append(i)
new_list = new_list


def do_it(new_list, k):
    print(k)
    vec = CountVectorizer(stop_words='english')
    X = vec.fit_transform(new_list).toarray()

    vocab = np.array(vec.get_feature_names())
    biterms = vec_to_biterms(X)

    btm = oBTM(num_topics=10, V=vocab)
    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100):
        print(i, len(biterms))
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=50)
    topics = btm.transform(biterms)
    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X, vocab, 10)
    topList = []
    # print("\n\n Texts & Topics ..")
    # for i in range(len(new_list)):
    #     print("{} (topic: {})".format(new_list[i], topics[i].argmax()))
    #     print(topics[i])
    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(
        X, axis=1), vocab, np.sum(X, axis=0))
    pyLDAvis.save_html(vis, './vis/online_btm.html')  # path to output


do_it(new_list[700:800], 8)
do_it(new_list[800:900], 9)
do_it(new_list[900:1000], 10)
do_it(new_list[1000:1100], 11)
do_it(new_list[1100:1200], 12)
do_it(new_list[1200:1300], 13)
do_it(new_list[1300:1400], 14)
do_it(new_list[1400:1500], 15)
do_it(new_list[1500:1600], 16)
do_it(new_list[1600:1700], 17)
do_it(new_list[1700:1800], 18)
do_it(new_list[1800:1900], 19)
do_it(new_list[1900:2000], 20)
