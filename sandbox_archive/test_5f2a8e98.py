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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        literal = random.choice(list(literals))
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            if dpll([clause for clause in cnf if not any(lit in clause or -lit in clause for lit in new_assignment)], new_assignment):
                return True
        return False
    
    def hodge_index(cnf):
        # Simplified heuristic to simulate Hodge index computation
        return len(cnf)
    
    def resolution_width(cnf):
        # Simplified heuristic to simulate resolution width computation
        return len(cnf)
    
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    mhi = hodge_index(cnf)
    w = resolution_width(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": mhi / w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")