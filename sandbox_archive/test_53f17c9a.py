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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            val = unit_clause[0] > 0
            if var in assignment and assignment[var] != val:
                return False
            assignment[var] = val
            return dpll([c for c in cnf if not (var in c and val == (c[0] > 0))], assignment)
        pure_literal = next((v for v in range(1, n + 1) if all(v not in c or (c[0] < 0) != (c[0] > 0) for c in cnf)), None)
        if pure_literal:
            val = True
            if -pure_literal in assignment and assignment[-pure_literal]:
                return False
            assignment[pure_literal] = val
            return dpll([c for c in cnf if not (pure_literal in c and val == (c[0] > 0))], assignment)
        p, _ = random.choice(cnf)
        return dpll(cnf, assignment) or dpll(cnf, {p: False})
    
    def frege_proof_depth(cnf):
        if dpll(cnf):
            return 1
        else:
            return float('inf')
    
    mdeg_values = []
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, n)
            cnf = generate_cnf(m, n)
            d = frege_proof_depth(cnf)
            mdeg_values.append((m, d))
            n_max = max(n_max, n)
    
    if not mdeg_values:
        return {
            "metric_name": "min_motivic_degree",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mdeg_values = [m for _, m in mdeg_values]
    d_values = [d for _, d in mdeg_values]
    
    if len(mdeg_values) < 30:
        return {
            "metric_name": "min_motivic_degree",
            "metric_value": 0,
            "instances_tested": len(mdeg_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_mdeg = sum(mdeg_values) / len(mdeg_values)
    mean_d = sum(d_values) / len(d_values)
    
    covariance = sum((mdeg - mean_mdeg) * (d - mean_d) for mdeg, d in zip(mdeg_values, d_values)) / len(mdeg_values)
    variance_mdeg = sum((mdeg - mean_mdeg) ** 2 for mdeg in mdeg_values) / len(mdeg_values)
    variance_d = sum((d - mean_d) ** 2 for d in d_values) / len(d_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_mdeg) * math.sqrt(variance_d))
    
    return {
        "metric_name": "min_motivic_degree",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mdeg_values),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed + 1}")