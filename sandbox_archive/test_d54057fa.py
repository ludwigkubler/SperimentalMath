# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            literals = [random.choice([i, -i]) for i in range(1, n+1)]
            clause = random.sample(literals, len(set(literals)))
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment[literal] = True
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            return dpll(cnf, new_assignment)
        
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            cnf = [c for c in cnf if pure_literal not in c and -pure_literal not in c]
            return dpll(cnf, new_assignment)
        
        if not cnf:
            return True
        literal = random.choice([l for l in range(1, n+1) if l not in assignment])
        new_assignment[literal] = True
        result = dpll(cnf, new_assignment)
        if result:
            return True
        del assignment[literal]
        new_assignment[-literal] = True
        return dpll(cnf, new_assignment)
    
    def geometric_entropy(curve):
        # Placeholder for actual geometric entropy calculation
        return random.random()  # Replace with actual computation
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            path_length = dpll(cnf)
            entropy = geometric_entropy(cnf)
            metric_values.append((entropy, path_length))
            instances_tested += 1
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Geometric Entropy vs DPLL Path Length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    correlation = 0
    mean_entropy = sum(x for x, _ in metric_values) / len(metric_values)
    mean_path_length = sum(y for _, y in metric_values) / len(metric_values)
    
    for entropy, path_length in metric_values:
        correlation += (entropy - mean_entropy) * (path_length - mean_path_length)
    
    correlation /= (len(metric_values) * sum((x - mean_entropy)**2 for x, _ in metric_values) ** 0.5 *
                    sum((y - mean_path_length)**2 for _, y in metric_values) ** 0.5)
    
    if correlation < 0.7:
        conjecture_holds = False
        counterexample = "Correlation coefficient below threshold"
    
    return {
        "metric_name": "Geometric Entropy vs DPLL Path Length",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")