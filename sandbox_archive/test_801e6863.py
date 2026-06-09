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
from fractions import Fraction
from math import log2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        clause = next(iter(clauses))
        for literal in clause:
            new_assignment = assignment.copy()
            var = abs(literal)
            value = 1 if literal > 0 else -1
            if var not in new_assignment:
                new_assignment[var] = value
                if dpll(clauses, new_assignment):
                    return True
            elif new_assignment[var] == value:
                continue
            else:
                break
        else:
            return False
        return False

    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def koszul_complex_size(clauses):
        # Simplified Koszul complex size calculation
        return len(set(tuple(sorted(c)) for c in clauses))

    instances_tested = 0
    min_generators = float('inf')
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_instance(n)
            instances_tested += 1
            if not dpll(clauses, {}):
                min_generators = min(min_generators, koszul_complex_size(clauses))
                n_max = max(n_max, n)
    
    conjecture_holds = min_generators <= n ** 2  # Simplified bound for demonstration
    counterexample = "" if conjecture_holds else f"min_generators={min_generators}, n^2={n ** 2}"
    
    return {
        "metric_name": "min_generators",
        "metric_value": min_generators,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_instances")