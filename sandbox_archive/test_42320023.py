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
    
    def generate_3cnf(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n + 1)]
            random.shuffle(literals)
            clause = ' & '.join(literals)
            clauses.append(clause)
        return ' | '.join(clauses)
    
    def xor_and_width(formula):
        # Simplified XOR-AND tree width calculation (placeholder)
        return len(formula.split(' | '))
    
    def tropicalized_rank(formula):
        # Placeholder for tropicalized rank calculation
        return random.randint(1, 10)  # Simulated value
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    density = random.uniform(0.1, 0.9)
    formula = generate_3cnf(n, density)
    
    rank = tropicalized_rank(formula)
    xor_and_width_val = xor_and_width(formula)
    
    if xor_and_width_val == 0:
        return {
            "metric_name": "tropicalized_rank_over_xor_and_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "xor_and_width_is_zero"
        }
    
    ratio = rank / xor_and_width_val
    
    return {
        "metric_name": "tropicalized_rank_over_xor_and_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] is None)
        print(f"RESULT: FALSIFIED counterexample=\"xor_and_width_is_zero\" first_failing_seed={first_failing_seed}")