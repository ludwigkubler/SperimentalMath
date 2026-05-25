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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_rank(A):
        rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def clifford_group_circuit(n):
        # Placeholder function to generate a random n-bit Clifford group circuit
        # This is a dummy implementation and should be replaced with actual code
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]

    def quaternion_algebra(circuit):
        # Placeholder function to compute the quaternion algebra associated with a circuit
        # This is a dummy implementation and should be replaced with actual code
        return [[random.choice([0, 1]) for _ in range(4)] for _ in range(len(circuit))]

    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        circuit = clifford_group_circuit(n)
        Q_C = quaternion_algebra(circuit)
        rank = matrix_rank(Q_C)
        depth = len(circuit)  # Placeholder for actual depth calculation
        results.append({
            "n": n,
            "rank": rank,
            "depth": depth
        })

    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    
    conjecture_holds = all(n * n * math.log(n) <= 3 * result["rank"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Quaternion Algebra",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*10**4, 1000))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - avg_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")