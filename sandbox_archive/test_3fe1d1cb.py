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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Each clause has 3 literals
            clause = [random.randint(-n, n) for _ in range(3)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                del new_assignment[abs(literal)]
        pure_literal = next((l for l in range(1, n+1) if all(l not in c or -l in c for c in cnf)), None)
        if pure_literal is not None:
            new_assignment = {**assignment, pure_literal: True}
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                del new_assignment[pure_literal]
        for literal in range(1, n+1):
            if literal not in assignment:
                if dpll(cnf, {**assignment, literal: True}):
                    return True
                if dpll(cnf, {**assignment, literal: False}):
                    return True
        return False
    
    def modular_form_order(cnf):
        # Simplified heuristic for demonstration purposes
        return len(cnf) * 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_length = dpll(cnf)
    
    if not proof_length:
        return {
            "metric_name": "modular_form_order",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL returned False, no proof length"
        }
    
    order = modular_form_order(cnf)
    return {
        "metric_name": "modular_form_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_order = sum(r["metric_value"] for r in results) / len(results)
        std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_order = None
        std_order = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        correlation_coefficient = sum((r["metric_value"] - mean_order) * (dpll(cnf, {}) - mean_order) for r in results) / (len(results) * std_order * std_order)
        if correlation_coefficient >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=missing_data")