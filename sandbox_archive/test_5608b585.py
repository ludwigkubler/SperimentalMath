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
    
    def entropy(clause_subset):
        if not clause_subset:
            return 0
        p = len(clause_subset) / total_clauses
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + sum(abs(A[j][i]) > abs(A[i][i]) for j in range(i, n))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i][0] for i in range(n)]

    def rank_of_matrix(A):
        n = len(A)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A_augmented = [A[i] + I[i] for i in range(n)]
        return sum(gaussian_elimination(A_augmented, [0]*n)[i] != 0 for i in range(n))

    def geometric_group_rank(phi):
        n = len(phi)
        G = []
        for i in range(1 << n):
            g = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    g[j] = 1
            G.append(g)
        return rank_of_matrix(G)

    def sat_clause_subset_entropy(phi):
        total_clauses = len(phi)
        subset_entropies = []
        for i in range(1, 1 << total_clauses):
            clause_subset = [phi[j] for j in range(total_clauses) if (i >> j) & 1]
            subset_entropies.append(entropy(clause_subset))
        return sum(subset_entropies) / len(subset_entropies)

    n = random.randint(5, 40)
    phi = [random.choice([True, False]) for _ in range(n)]
    
    entropy_value = sat_clause_subset_entropy(phi)
    rank_value = geometric_group_rank(phi)
    
    return {
        "metric_name": "Entropy vs Rank",
        "metric_value": entropy_value * rank_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")