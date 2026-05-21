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
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def max_singular_value(A):
        A = gaussian_elimination(A)
        singular_values = [abs(A[i][i]) for i in range(min(len(A), len(A[0])))]
        return max(singular_values)
    
    def generate_read_twice_bp(n):
        # Simplified model of a read-twice branching program
        bp = []
        for _ in range(2 * n):
            bp.append(random.choice([0, 1]))
        return bp
    
    def construct_transition_matrix(bp, n):
        M = [[0] * (n + 1) for _ in range(n + 1)]
        state = 0
        for bit in bp:
            if bit == 0:
                state = (state << 1) & ((1 << (n + 1)) - 1)
            else:
                state = ((state << 1) | 1) & ((1 << (n + 1)) - 1)
            M[state][state] += 1
        return M
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_read_twice_bp(n)
        M = construct_transition_matrix(bp, n)
        singular_value = max_singular_value(M)
        results.append({
            "n": n,
            "singular_value": singular_value
        })
    
    metric_name = "max_singular_value"
    metric_value = sum(result["singular_value"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["singular_value"] >= n for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, singular_value={results[0]['singular_value']} < {results[0]['n']}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")