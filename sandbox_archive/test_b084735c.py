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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def random_bp(size):
        bp = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
        return bp
    
    def read_twice_complexity(bp):
        n = len(bp)
        complexity = 0
        for i in range(n):
            for j in range(i+1, n):
                if bp[i][j] == 1:
                    complexity += 2
        return complexity
    
    def entanglement_entropy(bp):
        n = len(bp)
        size = n * (n - 1) // 2
        A = [[0 for _ in range(size)] for _ in range(size)]
        k = 0
        for i in range(n):
            for j in range(i+1, n):
                if bp[i][j] == 1:
                    A[k][k] += 1
                    for l in range(k+1, size):
                        A[l][l] += 1
                    k += 1
        
        det = determinant(A)
        if det == 0:
            return float('inf')
        
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        entropy = -rank * math.log(rank, 2)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            bp = random_bp(n)
            complexity = read_twice_complexity(bp)
            if complexity > 0:
                entropy = entanglement_entropy(bp)
                total_entropy += entropy
                instances_tested += 1
                if entropy >= n or (entropy < n and complexity < n**2):
                    conjecture_holds = False
                    counterexample = f"n={n}, BP complexity={complexity}, Entropy={entropy}"
    
    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else float('nan')
    support_fraction = instances_tested / (len(n_values) * 5)
    
    return {
        "metric_name": "Entanglement Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_entropy = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean_entropy = total_entropy / len(results) if len(results) > 0 else float('nan')
    support_fraction /= len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")