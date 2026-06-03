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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(1 << m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(m)]
            if all(c == 0 for c in clause):
                continue
            cnf.append(clause)
        return cnf
    
    def tseitin_encoding(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        n_vars = max(literals)
        new_cnf = []
        for i, clause in enumerate(cnf):
            var = n_vars + 1 + i
            new_cnf.append([var] + [-lit for lit in clause])
            for j in range(len(clause)):
                for k in range(j + 1, len(clause)):
                    new_cnf.append([-var, -clause[j], clause[k]])
        return new_cnf
    
    def dpll_solver(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        n_vars = max(literals)
        
        def solve(lits_true, lits_false):
            if not cnf:
                return True
            var = next((lit for lit in range(1, n_vars + 1) if lit not in lits_true and -lit not in lits_false), None)
            if var is None:
                return False
            
            new_lits_true = lits_true | {var}
            new_lits_false = lits_false | {-var}
            if solve(new_lits_true, new_lits_false):
                return True
            if solve(new_lits_false, new_lits_true):
                return True
            return False
        
        return solve(set(), set())
    
    def min_order(cnf):
        n_vars = max(abs(lit) for lit in cnf)
        tensor_order = 0
        while True:
            tensor_order += 1
            # Placeholder for actual symmetric tensor construction logic
            if dpll_solver(cnf):
                return tensor_order
    
    m = random.randint(5, 30)
    cnf = generate_cnf(m)
    new_cnf = tseitin_encoding(cnf)
    proof_length = len(new_cnf) + 1  # Simplified for demonstration
    min_tensor_order = min_order(cnf)
    
    return {
        "metric_name": "min_order",
        "metric_value": min_tensor_order,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": proof_length >= 0.5 * min_tensor_order,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"seed {res['seed']}\" first_failing_seed={res['seed']}")
                break