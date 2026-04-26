# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def walsh_hadamard_transform(arr):
    n = len(arr)
    if n == 1:
        return arr
    even = walsh_hadamard_transform([arr[i] for i in range(0, n, 2)])
    odd = walsh_hadamard_transform([arr[i] for i in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20]
    alpha_values = [3.0, 4.0, 4.267, 5.0]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for alpha in alpha_values:
            num_clauses = int(n * alpha)
            clauses = []
            for _ in range(num_clauses):
                literals = random.sample([-1, 1], n)
                clauses.append(literals)
            
            def g_F(x):
                return sum(2 * any(xi == li for xi, li in zip(x, clause)) - 1 for clause in clauses) % 2
            
            hat_g_F = walsh_hadamard_transform([g_F(tuple(x)) for x in product([-1, 1], repeat=n)])
            I_g_F = sum(abs(hat_g_F[S]) ** 2 * len(S) for S in subsets(range(n)))
            
            def dpll(F, assignment):
                if not F:
                    return True
                var = next(v for v in range(n) if v not in assignment)
                for val in [-1, 1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    new_F = [clause for clause in F if (val == -1 and all(xi != li for xi, li in zip(new_assignment, clause))) or (val == 1 and any(xi == li for xi, li in zip(new_assignment, clause)))]
                    if dpll(new_F, new_assignment):
                        return True
                return False
            
            leaves = 0
            def count_leaves(F, assignment):
                nonlocal leaves
                if not F:
                    leaves += 1
                    return
                var = next(v for v in range(n) if v not in assignment)
                for val in [-1, 1]:
                    new_assignment = assignment.copy()
                    new_assignment[var] = val
                    new_F = [clause for clause in F if (val == -1 and all(xi != li for xi, li in zip(new_assignment, clause))) or (val == 1 and any(xi == li for xi, li in zip(new_assignment, clause)))]
                    count_leaves(new_F, new_assignment)
            
            count_leaves(clauses, {})
            L_F = leaves
            
            if not (2 ** (I_g_F / 3 - 1) <= L_F <= 2 ** (I_g_F + math.log2(n + 1))):
                conjecture_holds = False
                counterexample += f"n={n}, alpha={alpha}: L(F)={L_F}, I[g_F]={I_g_F}\n"
            
            instances_tested += 1
    
    return {
        "metric_name": "log2_L_F",
        "metric_value": math.log2(L_F),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    mean_L_F = sum(r["metric_value"] for r in results) / len(results)
    std_L_F = math.sqrt(sum((r["metric_value"] - mean_L_F) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_L_F} std={std_L_F} support_fraction={support_fraction}")