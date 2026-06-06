# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import product

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1) for _ in range(random.randint(1, 3))]
        clauses.append(clause)
    return clauses

def dpll(cnf, literals=[]):
    if not cnf:
        return True
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_literals = [l for l in literals if l != -literal]
        if literal > 0:
            return dpll([c for c in cnf if literal not in c], new_literals + [literal])
        else:
            return dpll([c for c in cnf if -literal not in c], new_literals + [-literal])
    pure_literal = next((l for l in literals if all(l not in c or -l in c for c in cnf)), None)
    if pure_literal is None:
        return False
    new_literals = [l for l in literals if l != -pure_literal]
    if pure_literal > 0:
        return dpll([c for c in cnf if pure_literal not in c], new_literals + [pure_literal])
    else:
        return dpll([c for c in cnf if -pure_literal not in c], new_literals + [-pure_literal])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    length_dpll_proof = dpll(cnf)
    if length_dpll_proof is False:
        return {
            "metric_name": "DPLL Proof Length",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL proof failed"
        }
    
    # Placeholder for minimal order of unitary group (not implemented)
    min_order_unitary_group = 1
    
    O_phi = length_dpll_proof ** 2
    return {
        "metric_name": "O(φ)",
        "metric_value": O_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")