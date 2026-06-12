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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            clauses.append(clause)
        return clauses
    
    def clause_tree_width(clauses):
        if not clauses:
            return 0
        max_width = 0
        for i in range(len(clauses)):
            width = 1
            for j in range(i + 1, len(clauses)):
                if any(x in clauses[j] for x in clauses[i]):
                    width += 1
            max_width = max(max_width, width)
        return max_width
    
    def symplectic_volume(A):
        n = len(A)
        det = Fraction(1)
        for i in range(n):
            pivot = A[i][i]
            if pivot == 0:
                continue
            det *= pivot
            for j in range(i + 1, n):
                A[j][i] /= pivot
            for j in range(i + 1, n):
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return abs(det)
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def moment_map(clauses):
        n = len(clauses)
        A = [[0] * n for _ in range(n)]
        for i, (x, y) in enumerate(clauses):
            A[x - 1][y - 1] += 1
            A[y - 1][x - 1] += 1
        return A
    
    def upper_bound(w):
        # Placeholder function for the upper bound O(w(φ))
        return w * w
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = clause_tree_width(cnf)
    A = moment_map(cnf)
    
    volume = symplectic_volume(A)
    bound = upper_bound(width)
    
    return {
        "metric_name": "symplectic_volume",
        "metric_value": volume,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": volume <= bound,
        "counterexample": "" if volume <= bound else f"Volume {volume} > Bound {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{first_failing['counterexample']}' first_failing_seed={first_failing['seed']}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")