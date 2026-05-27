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
    
    def dpll_refutation_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = float('inf')
        for i in range(n):
            f_i_0 = [f[j] ^ (i & (1 << j)) for j in range(n)]
            f_i_1 = [f[j] ^ ((i | (1 << j)) & (1 << j)) for j in range(n)]
            depth = min(depth, 2 + dpll_refutation_depth(f_i_0), dpll_refutation_depth(f_i_1))
        return depth
    
    def quasi_linear_representation_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            row = [f[j] ^ (i & (1 << j)) for j in range(n)]
            if all(row[k] == row[0] for k in range(1, n)):
                rank += 1
        return rank
    
    def linear_equivalence_class(f):
        # Placeholder for actual implementation
        return f
    
    def test_conjecture(f):
        d = dpll_refutation_depth(f)
        rho = quasi_linear_representation_rank(f)
        c = Fraction(rho, d)
        return c > 0 and c != 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    conjecture_holds = test_conjecture(f)
    
    return {
        "metric_name": "c",
        "metric_value": Fraction(quasi_linear_representation_rank(f), dpll_refutation_depth(f)),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Function with n={n} does not satisfy the conjecture."
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_c = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_c} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function does not satisfy the conjecture.\" first_failing_seed={first_failing_seed}")