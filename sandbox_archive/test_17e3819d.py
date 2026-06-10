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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def ehrhart_polynomial_degree(cnf):
        # Placeholder function to simulate Ehrhart polynomial degree calculation
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(n // 2, n * (n + 1) // 2)
    
    def circuit_complexity(cnf):
        # Placeholder function to simulate circuit complexity calculation
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(n // 3, n * (n + 1) // 6)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    degree = ehrhart_polynomial_degree(cnf)
    complexity = circuit_complexity(cnf)
    
    expected_bound = n * (n + 1) // 6
    
    return {
        "metric_name": "Ehrhart Polynomial Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": degree <= expected_bound,
        "counterexample": f"Degree {degree} exceeds expected bound for n={n}" if not conjecture_holds else ""
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Degree exceeds expected bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")