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
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def circuit_depth(cnf):
        # Simplified DPLL solver to estimate circuit depth
        def dpll(model, cnf):
            if not cnf:
                return True
            literal = next((l for l in range(-n, n+1) if l not in model and -l not in model), None)
            if literal is None:
                return False
            new_model = model.copy()
            new_model[literal] = True
            if dpll(new_model, cnf):
                return True
            new_model.pop(literal)
            new_model[-literal] = True
            return dpll(new_model, cnf)
        
        depth = 0
        for _ in range(10):  # Simplified sampling
            model = {l: random.choice([True, False]) for l in range(-n, n+1)}
            if dpll(model, cnf):
                depth += 1
        return depth
    
    def minimal_order_p_adic(n):
        p = 2**n
        order = 0
        while p % 2 == 0:
            p //= 2
            order += 1
        return order
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    depth = circuit_depth(cnf)
    order = minimal_order_p_adic(n)
    
    if depth < order * math.log(p, 2):
        return {
            "metric_name": "Circuit Depth vs. Minimal Order",
            "metric_value": depth,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n} has lower depth {depth} than expected order {order}"
        }
    
    return {
        "metric_name": "Circuit Depth vs. Minimal Order",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 6)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n_max']}\" first_failing_seed={first_failing_seed}")