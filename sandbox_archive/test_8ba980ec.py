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
            A_S = [row[i] for i in S]
            disc = max(sum(abs(row[i]) for row in A_S) for i in range(n))
            if disc > max_disc:
                max_disc = disc
        return max_disc
    
    def simulate_protocol(A, n):
        leaves = set()
        for _ in range(2000):
            x = [bernoulli(1/2) for _ in range(n)]
            y = [bernoulli(1/2) for _ in range(n)]
            node = (x, y)
            while True:
                if any(x[i] == 1 and y[i] == 1 for i in range(n)):
                    leaves.add(node)
                    break
                else:
                    i = next(i for i in range(n) if x[i] == 1 and y[i] == 0)
                    node = (x[:i] + [1] + x[i+1:], y[:i] + [0] + y[i+1:])
        return len(leaves)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            pivot = next(j for j in range(i, n) if A[j][i])
            A[pivot], A[i] = A[i], A[pivot]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return A
    
    def norm_infinity(A):
        n = len(A)
        return max(sum(abs(row[i]) for row in A) for i in range(n))
    
    n_values = [4, 6, 8, 10, 12, 16, 20, 24, 32, 40]
    k_values = lambda n: min(5, math.floor(math.log2(n)) + 2)
    c = 1 / 8
    
    total_leaves = 0
    total_discs = 0
    instances_tested = 0
    
    for n in n_values:
        for k in range(2, k_values(n) + 1):
            A = [[bernoulli(1/2) for _ in range(n)] for _ in range(n)]
            disc_k = herdisc_k(A, k)
            leaves = simulate_protocol(A, n)
            total_leaves += leaves
            total_discs += disc_k
            instances_tested += 1
    
    mean_leaves = total_leaves / instances_tested
    mean_discs = total_discs / instances_tested
    support_fraction = sum(math.log2(leaves) >= k * disc_k / (8 * math.sqrt(k * math.log(n))) for n in n_values for k in range(2, k_values(n) + 1)) / (len(n_values) * k_values(n))
    
    if support_fraction >= 0.95:
        return {
            "metric_name": "log2(L(A))",
            "metric_value": mean_leaves,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        violating_triples = [(n, k) for n in n_values for k in range(2, k_values(n) + 1) if math.log2(leaves) < k * disc_k / (8 * math.sqrt(k * math.log(n)))]
        return {
            "metric_name": "log2(L(A))",
            "metric_value": mean_leaves,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"n={violating_triples[0][0]}, k={violating_triples[0][1]}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_leaves = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_leaves} support_fraction={support_fraction}")
    else:
        violating_triples = [(r["metric_name"], r["metric_value"], r["instances_tested"], r["conjecture_holds"], r["counterexample"]) for r in results if not r["conjecture_holds"]]
        print(f"RESULT: FALSIFIED counterexample=\"{violating_triples[0][4]}\" first_failing_seed={seeds[violation_index]}")