# auto-injected by SEC sandbox
import math
import itertools
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import json
from collections import defaultdict

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(x, y))

def build_cochain_complex(G):
    n = len(G)
    E_bi = []
    T_bi = []
    for i in range(n):
        for j in G[i]:
            for k in G[j]:
                if hamming_distance(i, k) <= 2:
                    E_bi.append((i, j, k))
                    T_bi.append((i, j, k))
    return E_bi, T_bi

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    h1_counts = defaultdict(int)
    h1_positive_probabilities = []
    
    for n in n_values:
        X = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
        G = {i: [j for j in range(len(X)) if hamming_distance(i, j) <= 1] for i in range(len(X))}
        
        E_bi, T_bi = build_cochain_complex(G)
        delta_0 = [[0] * len(E_bi) for _ in range(2**n)]
        delta_1 = [[0] * len(T_bi) for _ in range(len(E_bi))]
        
        for i in range(len(X)):
            for j in G[i]:
                if (i, j, k) in E_bi:
                    delta_0[i][E_bi.index((i, j, k))] += 1
                    delta_1[E_bi.index((i, j, k))][T_bi.index((i, j, k))] += 1
        
        ker_delta_1 = [sum(row) == 0 for row in delta_1]
        rank_delta_0 = sum(1 for row in delta_0 if any(x != 0 for x in row))
        
        h1 = sum(ker_delta_1) - rank_delta_0
        h1_counts[n] += h1
        h1_positive_probabilities.append(h1 > 0)
    
    empirical_mean_h1 = {n: h1_counts[n] / (2**n * 200) for n in n_values}
    fraction_positive_h1 = sum(h1_positive_probabilities) / len(n_values)
    
    conjecture_holds = all(empirical_mean_h1[n] <= 0.5 for n in n_values)
    counterexample = "" if conjecture_holds else "h^1(f) > 0 for some random f"
    
    return {
        "metric_name": "Pr[h^1(f)>0]",
        "metric_value": fraction_positive_h1,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_h1 = sum(result["metric_value"] for result in results) / len(results)
    std_h1 = (sum((result["metric_value"] - mean_h1) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_h1} std={std_h1} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) >= len(results) * 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"h^1(f) > 0 for some random f\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")