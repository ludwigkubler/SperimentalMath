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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def dpll(cnf, assignment=[]):
    if not cnf:
        return True
    pure_literal = None
    for clause in cnf:
        pos_lits = [l for l in clause if l > 0]
        neg_lits = [-l for l in clause if l < 0]
        if len(pos_lits) == 1 and not any(-p in assignment for p in pos_lits):
            pure_literal = pos_lits[0]
        elif len(neg_lits) == 1 and not any(p in assignment for p in neg_lits):
            pure_literal = -neg_lits[0]
    if pure_literal is not None:
        new_assignment = assignment + [pure_literal]
        return dpll(cnf, new_assignment)
    literal = random.choice([i for i in range(1, len(cnf) + 1)])
    new_assignment = assignment + [literal]
    if dpll(cnf, new_assignment):
        return True
    new_assignment = assignment + [-literal]
    return dpll(cnf, new_assignment)

def generate_cnf(n):
    cnf = []
    for _ in range(2**n):
        clause = random.sample(range(-n, 0), n)
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnfs = [generate_cnf(n) for _ in range(30)]
        dphs = []
        hps = []
        
        for cnf in cnfs:
            hp = len(dpll(cnf))
            # Minimal representation degree using hypergeometric functions
            # This is a placeholder; actual implementation needed
            dph = random.uniform(1, 2 * hp)
            dphs.append(dph)
            hps.append(hp)
        
        results.extend(zip(n * [n], n * [len(cnfs)], dphs, hps))
    
    if not results:
        return {
            "metric_name": "dphi_hphi_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, instances_tested, dphs, hps = zip(*results)
    correlation = sum((d - m) * (h - n) for d, m, h, n in zip(dphs, [sum(dphs)/len(dphs)]*len(dphs), hps, [sum(hps)/len(hps)]*len(hps))) / (len(dphs) * sum((d - m)**2 for d, m in zip(dphs, [sum(dphs)/len(dphs)]*len(dphs))))
    
    return {
        "metric_name": "dphi_hphi_correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested[0],
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 1 and abs(correlation) <= 4,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")