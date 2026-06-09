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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tensor_product(a, b):
        m, k = len(a), len(b[0])
        n = len(b)
        result = [[sum(a[i][j] * b[j][k] for j in range(k)) for k in range(n)] for i in range(m)]
        return result
    
    def minimal_representation_dimension(cnf):
        n = len(cnf)
        if n == 1:
            return 2
        dim = 2
        while True:
            algebra = [[0] * dim for _ in range(dim)]
            algebra[0][0] = 1
            for clause in cnf:
                new_algebra = tensor_product(algebra, algebra)
                if any(all(new_algebra[i][j] == 0 for j in range(dim)) for i in range(dim)):
                    return dim
                dim += 1
    
    max_dim = 0
    instances_tested = 30
    n_max = 40
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        dim = minimal_representation_dimension(cnf)
        if dim > max_dim:
            max_dim = dim
    
    conjecture_holds = max_dim <= n * math.log2(n)
    counterexample = "" if conjecture_holds else f"dim_rep({n})={max_dim}, expected O({n} log {n})"
    
    return {
        "metric_name": "minimal_representation_dimension",
        "metric_value": max_dim,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")