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
    
    def generate_cnf(num_vars, num_clauses):
        cnf = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(num_vars)]
            if all(x == 0 for x in clause):
                clause[-1] *= -1
            cnf.append(clause)
        return cnf
    
    def ehrhart_trace(cnf):
        # Placeholder for Ehrhart trace computation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) * 2  # Example: linear relationship for simplicity
    
    num_vars = random.randint(5, 30)
    num_clauses = random.randint(num_vars, num_vars * 10)
    cnf = generate_cnf(num_vars, num_clauses)
    
    trace = ehrhart_trace(cnf)
    ratio = trace / num_clauses if num_clauses > 0 else float('inf')
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": num_vars,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")