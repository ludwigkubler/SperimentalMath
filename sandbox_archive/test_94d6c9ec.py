# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def entropy(phi):
        total = sum(phi.values())
        return -sum(Fraction(count, total) * math.log2(Fraction(count, total)) for count in phi.values() if count > 0)

    def hodge_number(phi):
        n = len(phi)
        support = list(phi.keys())
        P = [Fraction(phi[x], n) for x in support]
        
        # Construct the associated complex curve
        points = [(x // (2 ** i)) % 2 for i in range(n)]
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            matrix[i][i] = 1
            for j in range(i + 1, n + 1):
                if points[j - 1] == points[i]:
                    matrix[i][j] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i + 1, m):
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
            return sum(1 for row in A if any(row[j] != 0 for j in range(n)))
        
        rank = gaussian_elimination(matrix)
        return n - rank
    
    def generate_boolean_function(n):
        return {x: random.choice([0, 1]) for x in range(n)}
    
    results = []
    for _ in range(30):
        phi = generate_boolean_function(random.randint(5, 40))
        hodge = hodge_number(phi)
        ent = entropy(phi)
        results.append((hodge, ent))
    
    mean_hodge = sum(h for h, _ in results) / len(results)
    mean_entropy = sum(e for _, e in results) / len(results)
    support_fraction = sum(1 for h, e in results if h <= e) / len(results)
    
    return {
        "metric_name": "Hodge number vs Entropy",
        "metric_value": mean_hodge,
        "instances_tested": 30,
        "n_max": max(len(phi) for phi, _ in results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else f"H^(1, 0)({phi}) = {mean_hodge}, Entropy({phi}) = {mean_entropy}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r >= 0.95 * max(results)) / len(results)
    
    if all(r >= 0.95 * max(results) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.95 * max(results) for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result < 0.95 * max(results))
        print(f"RESULT: FALSIFIED counterexample=\"H^(1, 0) > Entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")