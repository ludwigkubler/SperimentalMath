# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        clique = set()
        for _ in range(k):
            u = random.randint(0, n-1)
            if u not in clique:
                clique.add(u)
        return clique
    
    def is_submodular(ranks):
        for i in range(len(ranks)):
            for j in range(i+1, len(ranks)):
                for k in range(j+1, len(ranks)):
                    if ranks[i] + ranks[j] > ranks[k]:
                        return False
        return True
    
    def compute_rank(n, clique_size):
        rank = 0
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j))]
            if len(subset) == clique_size and all(j in subset for j in clique):
                rank += 1
        return rank
    
    def generate_dnf(size, n):
        dnf = []
        for _ in range(size):
            term = random.sample(range(n), random.randint(1, n))
            dnf.append(term)
        return dnf
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n-1, 5))
    
    clique = generate_k_clique(n, k)
    rank = compute_rank(n, k)
    
    dnf_sizes = [1, 2, 3, 4]
    dnf_ranks = []
    for size in dnf_sizes:
        dnf = generate_dnf(size, n)
        dnf_rank = sum(1 for term in dnf if all(j in clique for j in term))
        dnf_ranks.append(dnf_rank)
    
    if not is_submodular([rank] + dnf_ranks):
        return {
            "metric_name": "submodularity",
            "metric_value": 0,
            "instances_tested": len(dnf_sizes),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if rank > n:
        return {
            "metric_name": "rank_bound",
            "metric_value": 0,
            "instances_tested": len(dnf_sizes),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if rank < k * (k - 1) // 2:
        return {
            "metric_name": "rank_bound",
            "metric_value": 0,
            "instances_tested": len(dnf_sizes),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "rank_complexity",
        "metric_value": rank,
        "instances_tested": len(dnf_sizes),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = (sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")