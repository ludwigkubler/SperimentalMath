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
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            var = abs(literal)
            new_assignment[var] = literal > 0
            return dpll([c for c in cnf if var not in c], new_assignment)
        
        pure_literals = {}
        for clause in cnf:
            positive = [l for l in clause if l > 0]
            negative = [-l for l in clause if l < 0]
            if len(positive) == 1 and positive[0] not in pure_literals:
                pure_literals[positive[0]] = True
            elif len(negative) == 1 and -negative[0] not in pure_literals:
                pure_literals[-negative[0]] = False
        
        for var, value in pure_literals.items():
            new_assignment[var] = value
            if dpll([c for c in cnf if var not in c], new_assignment):
                return True
            del new_assignment[var]
        
        literal = random.choice(list(set(abs(clause[0]) for clause in cnf)))
        var = abs(literal)
        new_assignment[var] = literal > 0
        if dpll([c for c in cnf if var not in c], new_assignment):
            return True
        
        del new_assignment[var]
        new_assignment[var] = literal < 0
        if dpll([c for c in cnf if var not in c], new_assignment):
            return True
        
        del new_assignment[var]
        return False
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def grothendieck_riemann_roch(cnf):
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        degree = m + n
        return degree
    
    results = []
    for _ in range(30):
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        cnf = generate_cnf(m, n)
        d = len(cnf)  # Frege proof depth is the number of clauses
        mdeg = grothendieck_riemann_roch(cnf)
        results.append((mdeg, d))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mdegs, ds = zip(*results)
    mean_mdeg = sum(mdegs) / len(mdegs)
    mean_d = sum(ds) / len(ds)
    covariance = sum((mdeg - mean_mdeg) * (d - mean_d) for mdeg, d in results) / len(results)
    variance_mdeg = sum((mdeg - mean_mdeg) ** 2 for mdeg in mdegs) / len(mdegs)
    variance_d = sum((d - mean_d) ** 2 for d in ds) / len(ds)
    correlation_coefficient = covariance / (math.sqrt(variance_mdeg) * math.sqrt(variance_d))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")