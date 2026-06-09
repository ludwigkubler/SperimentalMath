# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(2, 3))]
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model):
        if not cnf:
            return True
        literal = next(l for l in range(1, n + 1) if l not in model and -l not in model)
        pos_clauses = [c for c in cnf if literal in c]
        neg_clauses = [c for c in cnf if -literal in c]
        if any(not solve(model | {literal}) for c in pos_clauses):
            return solve(model | {-literal})
        return False
    n = len(cnf[0])
    return solve({})

def lcai(cnf):
    def conformal_blocks(clause):
        if len(clause) == 2:
            return 1
        return sum(conformal_blocks(subclause) for subclause in combinations(clause, 2))
    
    pos_clauses = [c for c in cnf if all(l > 0 for l in c)]
    neg_clauses = [c for c in cnf if any(l < 0 for l in c)]
    return Fraction(sum(conformal_blocks(c) for c in pos_clauses), sum(conformal_blocks(c) for c in neg_clauses))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            lcai_value = lcai(cnf)
            h_phi = dpll(cnf)
            if h_phi:
                results.append((lcai_value, h_phi))
                instances_tested += 1
                n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "LCAI vs DPLL Height",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lcai_values, h_phi_values = zip(*results)
    mean_lcai = sum(lcai_values) / len(lcai_values)
    mean_diff = sum(abs(l - h) for l, h in zip(lcai_values, h_phi_values)) / len(lcai_values)
    correlation = (sum((l - mean_lcai) * (h - mean_h_phi) for l, h in zip(lcai_values, h_phi_values))
                   / (len(lcai_values) * sum((l - mean_lcai)**2 for l in lcai_values) ** 0.5
                      * sum((h - mean_h_phi)**2 for h in h_phi_values) ** 0.5))
    
    return {
        "metric_name": "LCAI vs DPLL Height",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")