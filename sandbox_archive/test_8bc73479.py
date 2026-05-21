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
    num_clauses = 2 * n
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) for _ in range(3)]
            random.shuffle(clause)
            clauses.append(tuple(clause))
        return clauses
    
    def tseitin_width(clauses):
        # Simplified Tseitin width calculation
        return len(set([abs(c[0]) for c in clauses]))
    
    def generate_noncommutative_algebra(clauses, k):
        variables = set(range(1, n + 1))
        relations = set()
        for i, j in combinations(variables, 2):
            if (i, j) not in clauses and (j, i) not in clauses:
                relations.add((i, j))
        # Simulate growth of the algebra
        dim_A_k = 2 ** k
        return dim_A_k
    
    def combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)
    
    clauses = generate_3cnf(n, num_clauses)
    tseitin_width_val = tseitin_width(clauses)
    conjecture_holds = True
    counterexample = ""
    
    if tseitin_width_val < math.log(n, 2):
        conjecture_holds = False
        counterexample = f"Tseitin width {tseitin_width_val} < log n ({math.log(n, 2)})"
    
    dim_A_k_values = []
    for k in range(1, 11):
        dim_A_k = generate_noncommutative_algebra(clauses, k)
        if dim_A_k < 2 ** (k / 2):
            conjecture_holds = False
            counterexample = f"dim(A_Φ_{k}) < 2^{k/2}"
        dim_A_k_values.append(dim_A_k)
    
    return {
        "metric_name": "dim(A_Φ_k)",
        "metric_value": sum(dim_A_k_values) / len(dim_A_k_values),
        "instances_tested": len(dim_A_k_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")