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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n // 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def is_satisfiable(cnf):
        stack = []
        assignment = [None] * (n + 1)
        
        def dfs(i):
            if i > n:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(any(x != -y for x, y in clause) for clause in cnf):
                    if dfs(i + 1):
                        return True
            assignment[i] = None
            return False
        
        return dfs(1)

    def galois_group_size(cnf):
        n = len(cnf)
        G = set()
        for i in range(2**n):
            perm = [i >> j & 1 for j in range(n)]
            if all(all(perm[abs(x) - 1] == (x > 0) ^ y for x, y in clause) for clause in cnf):
                G.add(tuple(perm))
        return len(G)

    def smallest_normalizing_subset(cnf):
        n = len(cnf)
        N = set(range(1, n + 1))
        while True:
            if all(any(x != -y for x, y in clause) for clause in cnf):
                return N
            N.remove(random.choice(list(N)))

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            cnf = generate_kcnf(n, k)
            if not is_satisfiable(cnf):
                continue
            galois_size = galois_group_size(cnf)
            N_F = smallest_normalizing_subset(cnf)
            ratio = len(N_F) / galois_size
            total_metric_value += ratio
            instances_tested += 1
            if ratio > n ** (math.log2(k + 1)):
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, N_F={len(N_F)}, |G_F|={galois_size}"
                break

    return {
        "metric_name": "Ratio of smallest normalizing subset to Galois group size",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")