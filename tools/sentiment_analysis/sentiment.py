from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from itertools import combinations, chain
import numpy as np
import pyLDAvis
import math

positive_list = open('../product-reviewB07H625JJL-five_star.txt',  'r')

new_list = []


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


def output_train(X, vectorizer, true_k=10, minibatch=False, showLable=False):
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    cluster_1 = []
    cluster_2 = []
    cluster_3 = []
    cluster1_semantic = 0
    cluster2_semantic = 0
    cluster3_semantic = 0

    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X))
    for j in range(len(result)):
        if result[j] == 0:
            cluster_1.append(new_list[j])
        # elif result[j] == 1:
        #     cluster_2.append(new_list[j])
        # elif result[j] == 2:
        #     cluster_3.append(new_list[j])

    vec = CountVectorizer(stop_words='english')
    X1 = vec.fit_transform(cluster_1).toarray()
    vocab = np.array(vec.get_feature_names())
    biterms = vec_to_biterms(X1)
    btm = oBTM(num_topics=10, V=vocab)
    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100):  # prozess chunk of 200 texts
        print('==>', i, len(biterms))
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=50)
    topics = btm.transform(biterms)
    # topics = btm.fit_transform(biterms, iterations=100)
    print("\n\n Visualize Topics ..")

    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X1, vocab, 10)
    print("\n\n Texts & Topics ..")
    for i in range(len(cluster_1)):
        print("{} (topic: {})".format(cluster_1[i], topics[i].argmax()))
    topics_file = open('./topic.text', 'a')
    topics_file.writelines(topics)

    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(
        X1, axis=1), vocab, np.sum(X1, axis=0))
    pyLDAvis.save_html(vis, './vis/online_btm.html')  # path to output

    return -km.score(X)


def open_file():
    file_list = ['../product-reviewB07H625JJL-one_star.txt', '../product-reviewB07H625JJL-two_star.txt',
                 '../product-reviewB07H625JJL-three_star.txt', '../product-reviewB07H625JJL-four_star.txt', '../product-reviewB07H625JJL-five_star.txt']
    # file_list = ['../product-reviewB07H625JJL-one_star.txt']
    for i in file_list:
        with open(i,  'r') as f:
            content = f.readlines()
            all_comment = 0
            positive_comment = 0
            for i in content:
                if i != '\n':
                    all_comment += 1
                    new_list.append(i)

    # vec = CountVectorizer(stop_words='english')
    # X = vec.fit_transform(new_list).toarray()
    # # get vocabulary
    # vocab = np.array(vec.get_feature_names())
    # # get biterms
    # biterms = vec_to_biterms(X)
    # # create btm
    # btm = oBTM(num_topics=10, V=vocab)
    # print("\n\n Train Online BTM ..")
    # for i in range(0, len(biterms), 100):  # prozess chunk of 200 texts
    #     print(i, len(biterms))
    #     biterms_chunk = biterms[i:i + 100]
    #     btm.fit(biterms_chunk, iterations=50)
    # topics = btm.transform(biterms)
    # print("\n\n Topic coherence ..")
    # topic_summuary(btm.phi_wz.T, X, vocab, 10)

    # print("\n\n Texts & Topics ..")
    # for i in range(len(new_list)):
    #     print("{} (topic: {})".format(new_list[i], topics[i].argmax()))
    # topics_file = open('./topic.text', 'a')
    # topics_file.writelines(topics)

    # print("\n\n Visualize Topics ..")
    # vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(
    #     X, axis=1), vocab, np.sum(X, axis=0))
    # pyLDAvis.save_html(vis, './vis/online_btm.html')  # path to output

# print(len(new_list))
    X, vectorizer = transform(new_list, n_features=500)
    output_train(X, vectorizer, true_k=3)


open_file()

# with open('../product-reviewB07H625JJL-one_star.txt',  'r') as f:
#     content = f.readlines()
#     all_comment = 0
#     positive_comment = 0
#     for i in content:
#         if i != '\n':
#             all_comment += 1
#             new_list.append(i)
#     for j in new_list:
#         if TextBlob(j).sentiment[0] > 0:
#             positive_comment += 1
#     X, vectorizer = transform(new_list, n_features=500)
#     true_ks = []
#     scores = []
#     for i in range(3, 80, 1):
#         score = output_train(X, vectorizer, true_k=i)
#         print(i, score)
#         true_ks.append(i)
#         scores.append(score)
#     plt.figure(figsize=(8, 4))
#     plt.plot(true_ks, scores, label="score", color="blue", linewidth=1)
#     plt.xlabel("n_features")
#     plt.ylabel("blue")
#     plt.legend()
#     plt.show()
# out = output_train(X, vectorizer, true_k=10, showLable=True)
# print(out)
# print(all_comment, positive_comment)
