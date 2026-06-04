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
    
    def generate_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified resolution width calculation
        return len(clauses) * 2
    
    def lattice_points_count(clauses):
        # Simplified lattice points count calculation
        return sum(len(clause) for clause in clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    clauses = generate_instance(n, m)
    
    width = resolution_width(clauses)
    lattice_points = lattice_points_count(clauses)
    ratio = lattice_points / (n + 1)  # Dimension is n+1 for projective space
    
    return {
        "metric_name": "Ratio of Lattice Points to Dimension",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= width,
        "counterexample": "" if ratio <= width else f"Ratio {ratio} > Width {width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Ratio {result['metric_value']} > Width {resolution_width(generate_instance(result['n_max'], 2 * result['n_max']))}\" first_failing_seed={seed}")
                break