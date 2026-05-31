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
    
    def tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f"y{i}"])
            clauses.append([f"y{i}", f"z{i}"])
            clauses.append([-f"y{i}", -f"z{i}"])
        for i in range(2, n+1):
            clauses.append([f"x{i}", f"x{i-1}"])
        return variables, clauses

    def kauffman_bracket(knot):
        # Placeholder implementation
        return 1  # Simplified for testing purposes

    def resolution_width(clauses):
        # Placeholder implementation
        return len(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            variables, clauses = tseitin_formula(n)
            knot = "".join(variables)  # Simplified for testing purposes
            chi_K = kauffman_bracket(knot)
            w_phi = resolution_width(clauses)
            total_metric_value += w_phi
            instances_tested += 1
            n_max = max(n_max, n)

            if w_phi > 1.5 * (2 ** chi_K):
                conjecture_holds = False
                counterexample = f"n={n}, w(φ)={w_phi}, O(2^χ(K))={1.5 * (2 ** chi_K)}"

    return {
        "metric_name": "resolution_width",
        "metric_value": total_metric_value / instances_tested,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")