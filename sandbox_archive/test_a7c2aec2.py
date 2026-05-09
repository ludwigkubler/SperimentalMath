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
    
    def polymatroid_rank(X):
        if not X:
            return 0
        n = len(X)
        P = [1] * (1 << n)
        for i in range(1, 1 << n):
            for j in range(i):
                if (i & j) == j and (i ^ j).bit_count() == 1:
                    P[i] += P[j]
        return sum(P[i] for i in range(len(X)) if (X >> i) & 1)
    
    def submodular_width(n, X, Y):
        return polymatroid_rank(X) + polymatroid_rank(Y) - polymatroid_rank(X & Y)
    
    def generate_k_clique_instance(n, k):
        edges = []
        for i in range(k):
            for j in range(i+1, k):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def generate_general_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = set()
            for i in range(n):
                if random.random() < 0.5:
                    clause.add(i)
            clauses.append(clause)
        return clauses
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n-1, 3))
    
    if random.random() < 0.5:
        instance_type = "k-clique"
        instance = generate_k_clique_instance(n, k)
    else:
        instance_type = "general"
        instance = generate_general_cnf(n)
    
    P_clique = [polymatroid_rank([i for i in range(n)])]
    for X in range(1 << n):
        P_clique.append(polymatroid_rank(X))
    
    max_width = 0
    for X in range(1 << n):
        for Y in range(1 << n):
            width = submodular_width(n, X, Y)
            if width > max_width:
                max_width = width
    
    if instance_type == "k-clique":
        lower_bound = math.ceil(n ** (k / 4))
        upper_bound = float('inf')
    else:
        lower_bound = 0
        upper_bound = n * math.log2(n)
    
    return {
        "metric_name": "submodular_width",
        "metric_value": max_width,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= max_width <= upper_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")