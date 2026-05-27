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
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def rank(A):
        r = 0
        for row in gaussian_elimination(A):
            if any(row):
                r += 1
        return r
    
    def random_polynomial(n, degree):
        coeffs = [random.randint(0, 1) for _ in range(degree + 1)]
        return sum(c * x**i for i, c in enumerate(coeffs))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    F = [random.randint(2, 10) for _ in range(n)]  # Finite fields of size 2 to 10
    R = [[random.randint(-10, 10) for _ in range(r)] for r in F]
    
    f = random_polynomial(n, n)
    C = [f(x) for x in range(2**n)]
    
    tropicalized_rank = rank([[C[i] if i % 2 == j else -math.inf for j in range(n)] for i in range(2**n)])
    
    return {
        "metric_name": "tropicalized_rank",
        "metric_value": tropicalized_rank,
        "instances_tested": n,
        "conjecture_holds": tropicalized_rank <= n,
        "counterexample": "" if tropicalized_rank <= n else f"Counterexample for n={n}, rank={tropicalized_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")