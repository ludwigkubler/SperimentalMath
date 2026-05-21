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
    
    def generate_k_clique(n, k):
        clique = set()
        for _ in range(k):
            node = random.randint(0, n-1)
            if node not in clique:
                clique.add(node)
        return clique
    
    def dnf_approximation(clique, epsilon):
        dnf_size = 0
        for node in range(len(clique)):
            dnf_size += 1
        return dnf_size * (1 + epsilon)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_dnf_size = 0
    instances_tested = 0
    
    for n in n_values:
        k = int(math.log(n))
        clique = generate_k_clique(n, k)
        dnf_size = dnf_approximation(clique, 0.1)
        total_dnf_size += dnf_size
        instances_tested += 1
    
    mean_dnf_size = total_dnf_size / len(n_values)
    
    if mean_dnf_size >= n:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "DNF size does not scale as Ω(n)"
    
    return {
        "metric_name": "mean_dnf_size",
        "metric_value": mean_dnf_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DNF size does not scale as Ω(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")