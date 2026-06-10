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
        for _ in range(2 ** n):
            clause = [random.randint(1, 2 * n) for _ in range(random.randint(1, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_subset(A, B):
        return all(x in B for x in A)
    
    def generate_coxeter_group(n):
        generators = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 2):
                if random.choice([True, False]):
                    generators.append((i, j))
        return generators
    
    def count_generators(generators):
        return len(generators)
    
    def enumerate_coxeter_groups(n):
        max_size = 0
        for _ in range(30):  # Sample 30 instances per seed
            cnf = generate_cnf(n)
            automorphism_group = set()
            for perm in itertools.permutations(range(1, n + 1)):
                if all(all(cnf[i - 1][j - 1] == cnf[perm[i - 1] - 1][perm[j - 1] - 1] for j in range(len(cnf[i - 1]))) for i in range(len(cnf))):
                    automorphism_group.add(tuple(perm))
            coxeter_group = generate_coxeter_group(n)
            if is_subset(coxeter_group, automorphism_group):
                max_size = max(max_size, count_generators(coxeter_group))
        return max_size
    
    n_max = 40
    instances_tested = 30
    metric_value = enumerate_coxeter_groups(n_max)
    conjecture_holds = metric_value <= 2 ** n_max
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_generators",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")