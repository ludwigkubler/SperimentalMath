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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cyclic_difference_set(f, n):
        diff_set = set()
        for i in range(2**n):
            diff = (i + 1) % (2**n)
            if f[i] != f[diff]:
                diff_set.add((i, diff))
        return diff_set
    
    def dpll_proof_width(f, n):
        # Simplified DPLL solver for demonstration purposes
        clauses = []
        for i in range(n):
            clauses.append([i])
            clauses.append([-i - 1])
        
        def solve(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment[:]
                new_assignment[abs(literal)] = literal > 0
                if solve(clauses, new_assignment):
                    return True
                else:
                    new_assignment[abs(literal)] = not (literal > 0)
                    if solve(clauses, new_assignment):
                        return True
            pure_literal = next((i for i in range(1, n + 1) if all(i in c or -i in c for c in clauses)), None)
            if pure_literal is not None:
                new_assignment[pure_literal] = True
                if solve(clauses, new_assignment):
                    return True
                else:
                    new_assignment[pure_literal] = False
                    if solve(clauses, new_assignment):
                        return True
            return False
        
        assignment = [False] * (n + 1)
        return len(solve(clauses, assignment))
    
    def minimal_rank(diff_set):
        # Simplified minimal rank calculation for demonstration purposes
        return len(diff_set)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    diff_set = cyclic_difference_set(f, n)
    proof_width = dpll_proof_width(f, n)
    rank = minimal_rank(diff_set)
    
    return {
        "metric_name": "correlation",
        "metric_value": rank / proof_width,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.9) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.9 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_less_than_0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")