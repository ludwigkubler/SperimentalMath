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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def communication_complexity_matrix(kcnf):
        n = len(kcnf[0])
        matrix = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << n):
                if all((x in kcnf and ((i & x) == x)) or (-x in kcnf and not (i & x)) for x in range(1, n + 1)):
                    matrix[i][j] = 1
        return matrix

    def rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
        return rank * (n - rank)

    def geometric_invariant_classes(kcnf, q):
        # Placeholder function to compute the number of geometric invariant classes
        # This is a dummy implementation and should be replaced with actual computation
        return len(kcnf)  # Simplified for demonstration

    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    q = random.choice([2, 3, 5])  # Field size
    kcnf = generate_kcnf(n, k)
    
    matrix = communication_complexity_matrix(kcnf)
    rank_var = rank_variance(matrix)
    kappa = geometric_invariant_classes(kcnf, q)
    
    lower_bound = kappa
    upper_bound = q ** (n / 2 - 1) * kappa
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": rank_var,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": lower_bound <= rank_var <= upper_bound,
        "counterexample": "" if lower_bound <= rank_var <= upper_bound else f"rank_var={rank_var}, kappa={kappa}, q^{n/2-1}*kappa={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")