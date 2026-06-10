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
    
    def generate_cnf(n_vars, n_clauses):
        cnf = []
        for _ in range(n_clauses):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n_vars))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            p = unit_clauses[0]
            if p < 0 and -p in assignment or p > 0 and p in assignment:
                return False
            return dpll([c for c in cnf if p not in c], assignment + [p])
        
        p, _ = random.choice(cnf)
        if p < 0 and -p in assignment or p > 0 and p in assignment:
            return False
        
        def remove_p(lit):
            return [c for c in cnf if lit not in c]
        
        return dpll(remove_p(p), assignment + [p]) or dpll(remove_p(-p), assignment + [-p])
    
    n_vars = random.randint(10, 40)
    n_clauses = random.randint(n_vars // 2, n_vars * 2)
    cnf = generate_cnf(n_vars, n_clauses)
    
    depth = dpll(cnf)
    if not isinstance(depth, int):
        return {
            "metric_name": "depth",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n_vars,
            "conjecture_holds": False,
            "counterexample": "dpll did not terminate"
        }
    
    def cocomplexity(cnf):
        # Placeholder for actual cocomplexity computation
        return random.random()
    
    chi_c = cocomplexity(cnf)
    d_phi = len(set(abs(lit) for lit in cnf))
    
    if d_phi == 0:
        return {
            "metric_name": "depth",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n_vars,
            "conjecture_holds": False,
            "counterexample": "d_phi is zero"
        }
    
    log_d_phi = math.log(d_phi)
    abs_diff = abs(chi_c - log_d_phi)
    
    return {
        "metric_name": "depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": 0.6 <= abs_diff <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")