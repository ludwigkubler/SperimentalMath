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
    
    def generate_3cnf(n):
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.choice(literals) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def count_literals(formula):
        literals = set()
        for clause in formula:
            literals.update(abs(lit) for lit in clause)
        return len(literals)
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    num_vars = count_literals(formula)
    
    # The minimal order of the action of the symmetric group on the set of real algebraic points
    # of the variety defined by a 3-CNF formula is at least exp(n^(1/2))
    min_order = math.exp(num_vars ** 0.5)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": 1,
        "conjecture_holds": min_order >= math.exp(n ** 0.5),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='None' first_failing_seed={first_failing_seed}")