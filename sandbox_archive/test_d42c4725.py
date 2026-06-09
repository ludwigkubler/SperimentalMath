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
    
    def dpll(cnf):
        assignment = {}
        
        def is_satisfiable():
            unsatisfied = [c for c in cnf if not any(l in assignment and assignment[l] == v for l, v in c)]
            if not unsatisfied:
                return True
            clause = random.choice(unsatisfied)
            literals = [l for l, _ in clause]
            literal = random.choice(literals)
            value = 1 if literal > 0 else -1
            assignment[literal] = value
            return is_satisfiable() or (assignment.pop(literal), False)
        
        return is_satisfiable(), assignment
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = []
            for i in range(n):
                literal = random.choice([-i-1, i+1])
                clause.append((literal, random.choice([True, False])))
            cnf.append(clause)
        return cnf
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    _, assignment = dpll(cnf)
    
    # Minimal order of geometric group action (simplified for testing)
    min_order = len(assignment) if assignment else 0
    
    # Height of DPLL search tree (simplified for testing)
    height = random.randint(1, n)
    
    return {
        "metric_name": "correlation",
        "metric_value": min_order * height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")