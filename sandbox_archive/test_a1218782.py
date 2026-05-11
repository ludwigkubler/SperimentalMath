# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bipartite_graph(n):
        U = list(range(n))
        V = list(range(n, 2*n))
        E = set()
        for u in U:
            for v in V:
                if random.choice([True, False]):
                    E.add((u, v))
        return (U, V, E)
    
    def clique_incidence_matrix(G):
        n = len(G[0])
        M = [[0] * (2*n) for _ in range(2*n)]
        for u in G[0]:
            for v in G[1]:
                if (u, v) in G[2]:
                    M[u][v+n] = 1
                    M[v+n][u] = 1
        return M
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = -1
            for i in range(rank, m):
                if A[i][j]:
                    i_max = i
                    break
            if i_max == -1:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank and A[i][j]:
                    factor = Fraction(A[i][j], A[rank][j])
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def communication_complexity(G):
        n = len(G[0])
        lower_bound = math.ceil(math.log2(n))
        return lower_bound
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_bipartite_graph(n)
    M = clique_incidence_matrix(G)
    rank = gaussian_elimination(M)
    cc = communication_complexity(G)
    
    return {
        "metric_name": "homotopy_group_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank == Fraction(1, cc),
        "counterexample": "" if rank == Fraction(1, cc) else f"n={n}, rank={rank}, CC(G)={cc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")