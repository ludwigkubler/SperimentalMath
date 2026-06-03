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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def search(assignment):
        unsatisfied_clauses = [c for c in cnf if not any(l in assignment or -l in assignment for l in c)]
        if not unsatisfied_clauses:
            return True
        pure_literal = next((l for l in range(1, n + 1) if all(l not in assignment and -l not in assignment for c in cnf)), None)
        if pure_literal is None:
            return False
        new_assignment = assignment.copy()
        new_assignment[pure_literal] = True
        if search(new_assignment):
            return True
        new_assignment[pure_literal] = False
        new_assignment[-pure_literal] = True
        return search(new_assignment)

    n = len(cnf[0]) // 2
    return search({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1))
        if not dpll(cnf):
            return {
                "metric_name": "O_c(φ) / log(n)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL proof not found"
            }
        O_c = len(cnf)
        L_phi = len(dpll(cnf))
        results.append((O_c, L_phi, n))
    
    if not results:
        return {
            "metric_name": "O_c(φ) / log(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid CNF found"
        }
    
    O_c_sum = sum(O_c for O_c, _, _ in results)
    L_phi_sum = sum(L_phi for _, L_phi, _ in results)
    n_sum = sum(n for _, _, n in results)
    mean_O_c = Fraction(O_c_sum, len(results))
    mean_L_phi = Fraction(L_phi_sum, len(results))
    mean_n = Fraction(n_sum, len(results))
    
    ratio_mean = mean_O_c / math.log(mean_n)
    correlation_coefficient = (sum((O_c - mean_O_c) * (L_phi - mean_L_phi) for O_c, L_phi, _ in results) /
                               math.sqrt(sum((O_c - mean_O_c)**2 for O_c, _, _ in results) *
                                         sum((L_phi - mean_L_phi)**2 for _, L_phi, _ in results)))
    
    return {
        "metric_name": "O_c(φ) / log(n)",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.95,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")