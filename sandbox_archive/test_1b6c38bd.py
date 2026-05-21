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
    
    n = 40
    k = 5
    
    # Generate a random 3-CNF formula with n variables and m clauses
    def generate_3cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n) * (1 if random.choice([True, False]) else -1)
                      for _ in range(3)]
            cnf.append(clause)
        return cnf
    
    # Convert 3-CNF to monotone DNF via resolution
    def resolve(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = set()
        while True:
            added = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-x in clauses[i] and x in clauses[j] for x in range(1, n + 1)):
                        new_clause = sorted([x for x in set(clauses[i]) | set(clauses[j]) if x > 0])
                        if new_clause not in clauses:
                            clauses.add(tuple(new_clause))
                            added = True
            if not added:
                break
        return [list(c) for c in clauses]
    
    cnf = generate_3cnf(2 * n)
    dnf = resolve(cnf)
    dnf_size = len(dnf)
    
    # Compute Fourier coefficients via Fast Walsh-Hadamard Transform
    def fast_walsh_hadamard_transform(x):
        N = len(x)
        if N == 1:
            return x
        even = fast_walsh_hadamard_transform(x[0::2])
        odd = fast_walsh_hadamard_transform(x[1::2])
        result = [0] * N
        for k in range(N // 2):
            result[k] = even[k] + odd[k]
            result[k + N // 2] = even[k] - odd[k]
        return result
    
    def fourier_coefficient(dnf, i):
        n = len(dnf)
        x = [1 if j == i else 0 for j in range(n)]
        transform = fast_walsh_hadamard_transform(x)
        return abs(transform[0])
    
    # Construct ρ(S) for all subsets S
    def polymatroid_rank(dnf, S):
        return sum(fourier_coefficient(dnf, i) for i in S)
    
    rho_n = polymatroid_rank(dnf, list(range(n)))
    max_rho_S = max(polymatroid_rank(dnf, S) for S in itertools.combinations(list(range(n)), 100))
    
    metric_name = "polymatroid_rank_bound"
    metric_value = rho_n
    instances_tested = 1
    conjecture_holds = rho_n >= math.sqrt(n) * k ** (1/4) and max_rho_S <= 10
    counterexample = "" if conjecture_holds else f"rho([n])={rho_n}, max_rho(S)={max_rho_S}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")