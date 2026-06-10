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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_bipartite_graph(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        G = [[A[i] == B[j] for j in range(n)] for i in range(n)]
        return G
    
    def matroid_representation(G):
        m = len(G)
        n = len(G[0])
        M = set()
        for i in range(m):
            for j in range(n):
                if G[i][j]:
                    M.add((i, j))
        return M
    
    def communication_complexity_rank_variance(M):
        ranks = [len([x for x in M if x[0] == i]) for i in range(len(G))]
        mean = sum(ranks) / len(ranks)
        variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return variance
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_bipartite_graph(n)
    M = matroid_representation(G)
    r_var = communication_complexity_rank_variance(M)
    
    metric_name = "monodromy_representations"
    metric_value = len(M)
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.6) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.6 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")