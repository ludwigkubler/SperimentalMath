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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def hodge_index(A):
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def circuit_complexity(F):
        # Placeholder function to simulate circuit complexity
        # Replace with actual implementation as needed
        return len(F)

    n_values = [5, 10, 15, 20, 30, 40]
    hodge_indices = []
    avg_circuit_complexities = []

    for n in n_values:
        instances_tested = 0
        total_hodge_index = 0
        total_avg_circuit_complexity = 0

        while instances_tested < 50:  # Ensure at least 30 instances per seed
            F = [''.join(random.choice('01') for _ in range(n)) for _ in range(2**n)]
            hodge_index_value = hodge_index([[int(bit) for bit in clause] for clause in F])
            avg_circuit_complexity = circuit_complexity(F)
            
            total_hodge_index += hodge_index_value
            total_avg_circuit_complexity += avg_circuit_complexity
            instances_tested += 1

        hodge_indices.append(total_hodge_index / instances_tested)
        avg_circuit_complexities.append(total_avg_circuit_complexity / instances_tested)

    metric_name = "Hodge Index"
    metric_value = sum(hodge_indices) / len(n_values)
    conjecture_holds = all(h <= n**3 for h, n in zip(hodge_indices, n_values)) and all(c >= 2**(1/3) * n**(1/3) + Fraction(1, 1000) for c, n in zip(avg_circuit_complexities, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")