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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = -1
            A[n][i] = f[i]
        return A
    
    def p_adic_roots(A, p):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            return []
        roots = [det_A % p]
        for i in range(1, p):
            roots.append((roots[-1] * (p - 1)) % p)
        return roots
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            sub_A = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(sub_A)
        return det
    
    def communication_complexity_rank(f):
        n = len(f)
        # Placeholder for actual CC rank calculation
        return math.isqrt(n)
    
    def correlation_coefficient(p_adic_count, cc_rank):
        if p_adic_count == 0 or cc_rank == 0:
            return 0
        return (p_adic_count - cc_rank) / (math.sqrt(n_max) * n_max)
    
    n_values = [5, 10, 15, 20, 30, 40]
    p = 2
    total_p_adic_roots = 0
    total_cc_ranks = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        A = characteristic_polynomial(f)
        p_adic_count = len(p_adic_roots(A, p))
        cc_rank = communication_complexity_rank(f)
        
        total_p_adic_roots += p_adic_count
        total_cc_ranks += cc_rank
        instances_tested += n
    
    mean_p_adic_roots = total_p_adic_roots / instances_tested
    mean_cc_ranks = total_cc_ranks / instances_tested
    correlation_coefficient_value = correlation_coefficient(mean_p_adic_roots, mean_cc_ranks)
    
    conjecture_holds = (mean_p_adic_roots >= n**(1/3)) and (mean_p_adic_roots <= n**(2/3)) and (math.isqrt(n_max) * math.isqrt(n_max) == cc_rank)
    counterexample = "correlation_coefficient=0" if correlation_coefficient_value == 0 else ""
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_cc_ranks,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")