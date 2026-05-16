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
    
    def bernoulli(p):
        return 1 if random.random() < p else 0
    
    def herdisc_k(A, k):
        n = len(A)
        max_disc = 0
        for S in itertools.combinations(range(n), k):
            disc = float('inf')
            for chi in itertools.product([-1, 1], repeat=k):
                A_S = [A[i][j] for i in range(n) for j in S if j == S.index(i)]
                norm = max(sum(A_S[j] * chi[j] for j in range(k)) for j in range(k))
                disc = min(disc, norm)
            max_disc = max(max_disc, disc)
        return max_disc
    
    def simulate_protocol_tree(A):
        n = len(A)
        leaves = set()
        
        def dfs(x, y, path):
            if all(x[i] != y[i] for i in range(n)):
                leaves.add(tuple(path))
                return
            for i in range(n):
                if x[i] == 1 and y[i] == 1:
                    dfs(x[:i] + (0,) + x[i+1:], y[:i] + (0,) + y[i+1:], path + [i])
                    dfs(x[:i] + (1,) + x[i+1:], y[:i] + (0,) + y[i+1:], path + [i])
                    break
        
        for i in range(2**n):
            x = tuple((i >> j) & 1 for j in range(n))
            y = tuple((i >> j) & 1 for j in range(n, 2*n))
            dfs(x, y, [])
        
        return len(leaves)
    
    n_values = [4, 6, 8, 10, 12, 16, 20, 24, 32, 40]
    k_values = range(2, math.floor(math.log2(n)) + 3)
    c = 1/8
    total_leaves = 0
    total_discs = 0
    num_trials = 0
    
    for n in n_values:
        for k in k_values:
            if k > 5:
                continue
            A = [[bernoulli(0.5) for _ in range(n)] for _ in range(n)]
            disc_k = herdisc_k(A, k)
            leaves = simulate_protocol_tree(A)
            total_leaves += leaves
            total_discs += disc_k * math.sqrt(k * math.log(n))
            num_trials += 1
    
    mean_leaves = total_leaves / num_trials
    std_dev = (sum((leaves - mean_leaves) ** 2 for leaves in [total_leaves]) / num_trials) ** 0.5
    support_fraction = sum(1 for leaves, disc_k in zip([total_leaves], [total_discs]) if math.log2(leaves) >= c * disc_k / (8 * math.sqrt(k * math.log(n)))) / len([total_leaves])
    
    return {
        "metric_name": "log2(L(A))",
        "metric_value": mean_leaves,
        "instances_tested": num_trials,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else f"n={n_values[0]}, k={k_values[0]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_leaves = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_leaves) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_leaves} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[0]}, k={k_values[0]}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")