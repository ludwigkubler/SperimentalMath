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
    
    def generate_cnf(n):
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        clauses = []
        for _ in range(n * (n - 1) // 2):
            clause = [random.choice(literals) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def circuit_depth(cnf):
        # Simplified DPLL solver to estimate circuit depth
        def dpll(model, cnf):
            if not cnf:
                return True
            literal = next((l for l in model if l != 0), None)
            if literal is None:
                return False
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                elif -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return False
                else:
                    new_clause = [l for l in clause if l != literal]
                    new_cnf.append(new_clause)
            return dpll(model + [literal], new_cnf) or dpll(model + [-literal], new_cnf)
        
        model = [0] * (2 * n)
        depth = 0
        while not dpll(model, cnf):
            model = [0] * (2 * n)
            depth += 1
        return depth
    
    def minimal_order_p_adic(n, p):
        # Compute the minimal order of a cyclic p-adic number in F_{2^n}
        if p <= 1:
            return None
        for k in range(1, n + 1):
            if (p ** k) % (2 ** n) == 1:
                return k
        return n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    depth = circuit_depth(cnf)
    p = random.choice([2, 3, 5, 7, 11])
    order = minimal_order_p_adic(n, p)
    
    if order is None:
        return {
            "metric_name": "circuit_depth",
            "metric_value": depth,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lower_bound = math.log(p ** n, 2)
    return {
        "metric_name": "circuit_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": depth >= lower_bound,
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
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")