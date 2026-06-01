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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literal = next((l for l in range(1, n + 1) if l not in model and -l not in model), None)
            if literal is None:
                return False
            model[literal] = True
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            if solve(model):
                return True
            del model[literal]
            model[-literal] = True
            new_cnf = [c for c in cnf if -literal not in c and literal not in c]
            return solve(model)
        n = len(cnf[0])
        return solve({})
    
    def hodge_index(cnf):
        # Placeholder implementation of Hodge index calculation
        # This is a dummy function that returns 0 for simplicity
        return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        dpll_diameter = dpll(cnf)
        hodge_index_value = hodge_index(cnf)
        
        if dpll_diameter == 0 or hodge_index_value == 0:
            continue
        
        results.append({
            "metric_name": "Hodge Index vs DPLL Diameter",
            "metric_value": abs(hodge_index_value) / dpll_diameter,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    return results[0] if results else {
        "metric_name": "Hodge Index vs DPLL Diameter",
        "metric_value": 0,
        "instances_tested": 1,
        "n_max": n_values[-1],
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
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
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='<not applicable>' first_failing_seed={first_failing_seed}")