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
    
    def dpll(clauses):
        if not clauses:
            return True
        clause = next(iter(clauses))
        for literal in clause:
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses):
                return True
        return False
    
    def frege_proof_depth(clauses):
        return len(dpll(clauses))  # Simplified for testing purposes
    
    def tseitin_variety(clauses, variables):
        n = len(variables)
        monoids = {var: set() for var in variables}
        for clause in clauses:
            new_var = f"v{len(monoids)}"
            monoids[new_var] = {new_var}
            for literal in clause:
                if literal > 0:
                    monoids[literal].add(new_var)
                else:
                    monoids[-literal].add(f"{new_var}_neg")
        return monoids
    
    def grothendieck_folds(monoids):
        folds = set()
        for monoid in monoids.values():
            for a, b in itertools.combinations(monoid, 2):
                if a < b:
                    folds.add((a, b))
        return len(folds)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_folds = 0
    total_depths = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables = list(range(1, n + 1))
            clauses = [random.sample(variables, random.randint(1, n)) for _ in range(n)]
            monoids = tseitin_variety(clauses, variables)
            folds = grothendieck_folds(monoids)
            depth = frege_proof_depth(clauses)
            total_folds += folds
            total_depths += depth
            instances_tested += 1
    
    mean_fold = total_folds / instances_tested
    mean_depth = total_depths / instances_tested
    alpha = mean_fold / mean_depth if mean_depth != 0 else float('inf')
    
    return {
        "metric_name": "alpha",
        "metric_value": alpha,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(alpha) <= 1.5,
        "counterexample": "" if abs(alpha) <= 1.5 else f"alpha={alpha} > 1.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_alpha = sum(r["metric_value"] for r in results) / len(results)
    std_alpha = math.sqrt(sum((r["metric_value"] - mean_alpha) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) <= 1.5) / len(results)
    
    if all(abs(r["metric_value"]) <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha} std={std_alpha} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 1.5 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if abs(r["metric_value"]) > 1.5)
        print(f"RESULT: FALSIFIED counterexample='alpha={r['metric_value']} > 1.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")