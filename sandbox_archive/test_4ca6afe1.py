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
    
    def generate_cnf(n: int):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def hodge_tate_degree(cnf: list):
        # Simplified heuristic to approximate Hodge-Tate degree
        return len(cnf) / 2
    
    def sat_clause_subset_complexity(cnf: list):
        # Simplified heuristic to approximate SAT clause subset complexity
        return sum(len(clause) for clause in cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        htd = hodge_tate_degree(cnf)
        csc = sat_clause_subset_complexity(cnf)
        results.append((n, htd, csc))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    htd_values = [r[1] for r in results]
    csc_values = [r[2] for r in results]
    
    mean_htd = sum(htd_values) / len(htd_values)
    mean_csc = sum(csc_values) / len(csc_values)
    
    correlation_coefficient = sum((htd - mean_htd) * (csc - mean_csc) for htd, csc in zip(htd_values, csc_values)) / \
                              math.sqrt(sum((htd - mean_htd)**2 for htd in htd_values) *
                                        sum((csc - mean_csc)**2 for csc in csc_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.7 <= correlation_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE some trials did not generate any instances")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if 0.7 <= r["metric_value"] < 0.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")