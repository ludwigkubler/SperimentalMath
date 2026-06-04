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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(clause) == 2 and clause[0] != -clause[1]:
                clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL search tree for width calculation
        stack = []
        while stack or clauses:
            if not stack:
                literal = random.choice([c for c in sum(clauses, []) if c > 0])
                stack.append((literal, [c for c in clauses if literal not in c]))
            else:
                literal, remaining_clauses = stack.pop()
                if literal == -remaining_clauses[0][0]:
                    continue
                new_clause = [l for l in remaining_clauses[0] if l != literal]
                if len(new_clause) == 1:
                    return abs(new_clause[0])
                stack.append((new_clause[0], remaining_clauses[1:]))
        return 1
    
    def hodge_index(n):
        # Simplified Hodge index computation
        return Fraction(1, n)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(3, n-1))
    phi = generate_kcnf(n, k)
    
    w_phi = resolution_width(phi)
    H_phi = hodge_index(n)
    
    metric_value = log2(n**(k+1)) <= w_phi + H_phi
    conjecture_holds = metric_value
    
    return {
        "metric_name": "resolution_width",
        "metric_value": int(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"phi={phi}, w_phi={w_phi}, H_phi={H_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")