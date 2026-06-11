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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for i in range(1, p):
            if (i * i) % p == a:
                return True
        return False
    
    def count_quadratic_residues(p):
        return sum(is_quadratic_residue(a, p) for a in range(p))
    
    def dpll(cnf):
        if not cnf:
            return True
        if any(len(clause) == 0 for clause in cnf):
            return False
        
        # Select the first variable to branch on
        var = next(iter(cnf[0]))
        
        # Create new CNF instances by branching on the selected variable
        true_cnf = [clause for clause in cnf if var not in clause]
        false_cnf = [clause for clause in cnf if -var not in clause]
        
        return dpll(true_cnf) or dpll(false_cnf)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(range(-n, 0), 1) + random.sample(range(1, n + 1), 1)
            clauses.append(clause)
        return clauses
    
    n = 30
    cnf = generate_cnf(n)
    
    p = 2 ** (n * n)
    residues_count = count_quadratic_residues(p)
    log_residues = math.log(residues_count, 2)
    
    dpll_height = dpll(cnf)
    
    if dpll_height is None:
        return {
            "metric_name": "DPLL height",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll returned None"
        }
    
    return {
        "metric_name": "DPLL height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(dpll_height - log_residues) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
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
    elif any(abs(r["metric_value"] - math.log(count_quadratic_residues(2**(30*30)), 2)) > 3 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - math.log(count_quadratic_residues(2**(30*30)), 2)) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"dpll_height does not match log_residues\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")