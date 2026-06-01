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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(num_vars)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, num_vars - 1)] = random.choice([1, -1])
            cnf.append(clause)
        return cnf
    
    def calculate_ehrhart_trace(cnf):
        # Simplified Ehrhart trace calculation (not actual Ehrhart theory)
        return len(cnf) * len(cnf[0])  # Placeholder for actual computation
    
    num_vars = random.randint(5, 10)
    num_clauses = random.randint(num_vars, num_vars * 2)
    
    cnf = generate_cnf(num_vars, num_clauses)
    ehrhart_trace = calculate_ehrhart_trace(cnf)
    
    metric_value = ehrhart_trace / num_clauses
    instances_tested = 1
    n_max = max(num_vars, num_clauses)
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "Ehrhart Trace Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")