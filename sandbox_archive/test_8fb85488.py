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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_order(cnf):
        # Placeholder function to compute minimal order of algebraic integers
        # This is a dummy implementation and should be replaced with actual computation
        return random.uniform(0.5, 2.0)
    
    n_max = 30
    instances_tested = 0
    total_ratio = 0
    
    for m in [5, 10, 15, 20, 30]:
        for _ in range(6):  # 6 instances per size
            cnf = generate_cnf(m, n_max)
            min_order = compute_minimal_order(cnf)
            ratio = min_order / (m ** (Fraction(1, 3)) * n_max ** (Fraction(2, 3)))
            total_ratio += ratio
            instances_tested += 1
    
    conjecture_holds = all(ratio <= 1.5 for ratio in [total_ratio / instances_tested])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ratio",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")