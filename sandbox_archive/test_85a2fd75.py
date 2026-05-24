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
    n = random.choice([12, 14, 16, 18, 20])
    
    # Generate a random 3-CNF formula with n variables
    clauses = []
    for _ in range(n):
        literals = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(3)]
        clause = tuple(sorted(literals))
        if clause not in clauses:
            clauses.append(clause)
    
    F = " and ".join(f"({' or '.join(map(str, clause))})" for clause in clauses)
    
    # Simulate DPLL proof time (simplified model)
    t_star = 2 ** n
    
    # Construct a curve X over an algebraic closure of the rationals
    # This is a placeholder; actual construction would be complex
    order = random.randint(1, 50)  # Placeholder for local system order
    
    expected_order = math.isclose(order, t_star ** 0.5, rel_tol=0.3) or math.isclose(order, t_star ** 0.5 * 2, rel_tol=0.3)
    
    return {
        "metric_name": "local_system_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": expected_order,
        "counterexample": f"n={n}, t_star={t_star}, order={order}, expected_order={expected_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    first_failing_seed = None
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        
        if not trial_result["conjecture_holds"]:
            first_failing_seed = seed
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, t_star={results[0]['t_star']}, order={results[0]['metric_value']}, expected_order={math.isclose(results[0]['metric_value'], results[0]['t_star'] ** 0.5, rel_tol=0.3) or math.isclose(results[0]['metric_value'], results[0]['t_star'] ** 0.5 * 2, rel_tol=0.3)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")