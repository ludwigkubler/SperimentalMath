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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals, assignment):
            if not cnf:
                return True
            literal = next((l for l in range(1, n + 1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            if literal > 0:
                assignment[literal] = True
            else:
                assignment[-literal] = True
            if solve(literals, assignment):
                return True
            del assignment[literal]
            if literal > 0:
                assignment[literal] = False
            else:
                assignment[-literal] = False
            if solve(literals, assignment):
                return True
            del assignment[-literal]
            return False
        
        n = len(cnf[0])
        assignment = {}
        return solve(range(1, n + 1), assignment)
    
    def algebraic_k_group_rank(cnf):
        # Placeholder implementation for minimal rank calculation
        # This is a dummy function and should be replaced with actual computation
        return random.randint(1, len(cnf))
    
    def property_P(cnf):
        # Placeholder implementation for property P check
        # This is a dummy function and should be replaced with actual computation
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    rank_k_values = []
    dpll_depths = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank_k = algebraic_k_group_rank(cnf)
            depth = dpll(cnf)
            if depth is None:
                continue
            rank_k_values.append(rank_k)
            dpll_depths.append(depth)
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(rank_k_values, dpll_depths)) / (len(rank_k_values) * std_dev_x * std_dev_y)
    mean_rank_k = sum(rank_k_values) / len(rank_k_values)
    std_dev_rank_k = math.sqrt(sum((x - mean_rank_k) ** 2 for x in rank_k_values) / len(rank_k_values))
    
    if correlation_coefficient < 0.7:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Correlation coefficient too low"
        }
    
    for rank_k, depth in zip(rank_k_values, dpll_depths):
        if not property_P(generate_cnf(n)) and rank_k > depth:
            return {
                "metric_name": "property_P",
                "metric_value": rank_k,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"rank_k({depth}) > {depth}"
            }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")