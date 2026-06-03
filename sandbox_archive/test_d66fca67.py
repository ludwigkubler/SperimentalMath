# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (2 * random.randint(0, 1) - 1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        n = len(cnf)
        literals = list(range(1, n + 1)) + [-l for l in range(1, n + 1)]
        
        def solve(lits, cls):
            if not cls:
                return True
            pure_literal = next((l for l in lits if all(l not in c or -l not in c for c in cls)), None)
            if pure_literal is not None:
                new_lits = [l for l in lits if l != pure_literal and l != -pure_literal]
                return solve(new_lits, cls)
            unit_clause = next((c for c in cls if len(c) == 1), None)
            if unit_clause is not None:
                literal = unit_clause[0]
                new_cls = [c for c in cls if literal not in c and -literal not in c]
                return solve(lits, new_cls)
            p_literal = random.choice(literals)
            new_lits_true = lits + [p_literal]
            new_lits_false = lits + [-p_literal]
            return solve(new_lits_true, cls) or solve(new_lits_false, cls)
        
        return 1 if solve(literals, cnf) else 0
    
    def local_indeterminacy(cnf):
        n = len(cnf)
        rank = 0
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clause = [i, -j]
                if all(l not in c or -l not in c for c in cnf):
                    rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, int(1.5 * n))
            depth = dpll(cnf)
            lcoh = local_indeterminacy(cnf)
            results.append((n, depth, lcoh))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, depths, lcohs = zip(*results)
    mean_depth = sum(depths) / len(depths)
    mean_lcoh = sum(lcohs) / len(lcohs)
    correlation_coefficient = (sum((d - mean_depth) * (l - mean_lcoh) for d, l in zip(depths, lcohs)) /
                               math.sqrt(sum((d - mean_depth)**2 for d in depths) *
                                         sum((l - mean_lcoh)**2 for l in lcohs)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(l <= math.sqrt(d) + 1 for d, l in zip(depths, lcohs)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")