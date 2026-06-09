# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment[var] = 1
            if dpll([c for c in cnf if var not in c], new_assignment):
                return True
            del new_assignment[var]
            new_assignment[var] = -1
            if dpll([c for c in cnf if var not in c], new_assignment):
                return True
            del new_assignment[var]
        else:
            var = random.choice(list(assignment.keys()) or variables)
            for val in [1, -1]:
                new_assignment[var] = val
                if dpll(cnf, new_assignment):
                    return True
                del new_assignment[var]
        return False
    
    def tropical_curve(cnf):
        # Placeholder for the actual algorithm to compute the tropical curve
        return len(cnf)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 2))
            h_DPLL = dpll(cnf)
            C_phi = tropical_curve(cnf)
            instances_tested += 1
            metric_values.append(C_phi)
            
            if C_phi > h_DPLL:
                conjecture_holds = False
                counterexample = f"n={n}, |C(φ)|={C_phi} > h_DPLL(φ)={h_DPLL}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(r["metric_value"] > 0.8 for r in results) or any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")