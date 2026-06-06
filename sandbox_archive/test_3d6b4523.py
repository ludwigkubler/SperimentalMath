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

def generate_cnf(n):
    cnf = []
    for _ in range(2**n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll(cnf, new_literals=[]):
    unit_clause = next((c for c in cnf if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        return dpll([c for c in cnf if -literal not in c], new_literals + [literal])
    
    if not cnf:
        return True
    
    literal = next((l for l in range(1, n+1) if all(l not in clause and -l not in clause for clause in cnf)), None)
    if literal is None:
        return False
    
    return dpll([c for c in cnf if -literal not in c], new_literals + [literal]) or dpll(cnf, new_literals + [-literal])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    cnf = generate_cnf(n)
    length_dpll_proof = dpll(cnf)
    
    if length_dPLL_proof is None:
        return {
            "metric_name": "O(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length not finite"
        }
    
    O_phi = Fraction(length_dpll_proof, 2)
    
    return {
        "metric_name": "O(φ)",
        "metric_value": float(O_phi),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")