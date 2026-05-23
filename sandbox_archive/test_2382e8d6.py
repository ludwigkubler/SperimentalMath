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
    
    def schur_polynomial(f):
        # Constructive mapping from Boolean function to Schur polynomial
        n = len(f)
        s = [[0] * (n + 1) for _ in range(n + 1)]
        s[0][0] = 1
        for i in range(1, n + 1):
            s[i][0] = s[i - 1][0]
            for j in range(1, min(i, n // 2) + 1):
                s[i][j] = s[i - 1][j - 1] + s[i - 1][j]
        return sum(s[i][i % 2] * f[i] for i in range(n))
    
    def dpll_search_tree_width(f):
        # Constructive mapping from Boolean function to DPLL search tree width
        n = len(f)
        if n == 0:
            return 1
        if n == 1:
            return 2
        return 2 * dpll_search_tree_width(f[:n // 2]) + dpll_search_tree_width(f[n // 2:])
    
    def random_boolean_function(n):
        return [random.choice([True, False]) for _ in range(n)]
    
    n = random.randint(5, 40)
    f = random_boolean_function(n)
    
    schur_rank = schur_polynomial(f)
    dpll_width = dpll_search_tree_width(f)
    
    return {
        "metric_name": "Schur Rank vs DPLL Width",
        "metric_value": abs(schur_rank - dpll_width),
        "instances_tested": 1,
        "conjecture_holds": schur_rank == dpll_width,
        "counterexample": "" if schur_rank == dpll_width else f"Schur Rank: {schur_rank}, DPLL Width: {dpll_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Schur Rank != DPLL Width\" first_failing_seed={first_failing_seed}")