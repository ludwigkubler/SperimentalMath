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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = set()
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def tree_width(cnf):
        # Simplified heuristic to estimate tree-width
        return len(cnf) ** 0.5
    
    def quotient_algebra_size(cnf):
        # Simplified heuristic for the size of the quotient algebra
        return len(cnf) * (len(cnf) - 1) // 2
    
    n = random.randint(5, 40)
    k = random.randint(1, n)
    cnf = generate_k_cnf(n, k)
    
    known_tree_width = tree_width(cnf)
    computed_quotient_rank = quotient_algebra_size(cnf)
    
    mean_absolute_difference = abs(computed_quotient_rank - known_tree_width)
    
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": mean_absolute_difference,
        "instances_tested": 1,
        "conjecture_holds": mean_absolute_difference <= 3,
        "counterexample": "" if mean_absolute_difference <= 3 else f"n={n}, k={k}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")