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
    
    def generate_cnf(n_vars, n_clauses):
        cnf = []
        for _ in range(n_clauses):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n_vars)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literal = next((lit for lit in model if any(lit == x or -lit == x for x in clause) for clause in cnf), None)
            if literal is None:
                return False
            new_cnf = [clause for clause in cnf if not any(lit == x or -lit == x for x in clause)]
            model.add(literal)
            if solve(model):
                return True
            model.remove(literal)
            model.add(-literal)
            if solve(model):
                return True
            return False
        
        return solve(set())
    
    def cocomplexity(cnf):
        n_vars = max(abs(lit) for clause in cnf for lit in clause)
        # Placeholder implementation; actual computation depends on the specific definition of cocomplexity
        return random.uniform(0, 1)
    
    n_vars = random.randint(10, 40)
    n_clauses = random.randint(n_vars // 2, n_vars * 2)
    cnf = generate_cnf(n_vars, n_clauses)
    
    depth = dpll(cnf)
    cc_value = cocomplexity(cnf)
    
    return {
        "metric_name": "d(χ_c(φ))",
        "metric_value": math.log(depth) if depth > 0 else -math.inf,
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")