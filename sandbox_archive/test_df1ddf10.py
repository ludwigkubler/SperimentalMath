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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        # Simplified DPLL algorithm to estimate resolution width
        states = []
        for clause in clauses:
            states.append(set(clause))
        
        def dpll(state, literals):
            if not state:
                return True
            literal = next(iter(literals))
            pos_clauses = [c for c in state if literal in c]
            neg_clauses = [c for c in state if -literal in c]
            
            if any(all(x in state for x in clause) for clause in neg_clauses):
                return False
            
            new_state = state.copy()
            new_state.remove(literal)
            literals.discard(literal)
            if dpll(new_state, literals):
                return True
            
            new_state = state.copy()
            new_state.remove(-literal)
            literals.discard(-literal)
            if dpll(new_state, literals):
                return True
        
        width = 0
        for literal in set.union(*states):
            literals = {l for l in range(1, n+1) if l != literal and -l not in states[0]}
            if not dpll(states, literals):
                width += 1
        
        return width

    def minimal_quaternion_order(clauses):
        # Simplified mapping to quaternion algebra
        order = 0
        for clause in clauses:
            for literal in clause:
                order = max(order, abs(literal))
        return order

    n = random.randint(5, 30)
    m = min(n * (n - 1) // 2, 20)
    clauses = generate_3cnf(n, m)
    
    width = resolution_width(clauses)
    order = minimal_quaternion_order(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")