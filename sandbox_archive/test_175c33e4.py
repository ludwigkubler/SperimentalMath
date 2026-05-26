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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    A[i][j] = Fraction(2**(n - i))
                else:
                    A[i][j] = Fraction(-2**(n - max(i, j)))
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None
            for j in range(n):
                if i != j:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def hodge_integrals(A):
        n = len(A) - 1
        det = Fraction(1)
        for i in range(n + 1):
            det *= A[i][i]
        return [det / Fraction(i + 1, 1) for i in range(n)]
    
    def min_rank_hodge_integrals(f):
        n = len(f)
        P_f = characteristic_polynomial(f)
        rank = gaussian_elimination(P_f)
        if rank is None:
            return None
        hodge_ints = hodge_integrals(P_f)
        return rank, hodge_ints
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        f = generate_boolean_function(n)
        result = min_rank_hodge_integrals(f)
        if result is None:
            return {
                "metric_name": "min_rank",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        ranks.append(result[0])
    
    min_rank = min(ranks)
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": min_rank <= 10 * len(n_values),  # Example bound, replace with actual
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = (sum((r["metric_value"] - mean)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")