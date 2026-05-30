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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dpll_refutation_size(f):
        n = len(f)
        clauses = [f[i:i + n] for i in range(0, len(f), n)]
        stack = []
        assignment = {}
        
        def solve():
            if not clauses:
                return True
            literal = next((l for l in range(n) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                if any(l in assignment and assignment[l] == True for l in clause):
                    continue
                elif any(-l in assignment and assignment[-l] == True for l in clause):
                    return False
                else:
                    new_clauses.append(clause)
            stack.append((literal, new_clauses))
            
            if solve():
                return True
            
            del assignment[literal]
            literal = -literal
            assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                if any(l in assignment and assignment[l] == True for l in clause):
                    continue
                elif any(-l in assignment and assignment[-l] == True for l in clause):
                    return False
                else:
                    new_clauses.append(clause)
            stack.append((literal, new_clauses))
            
            if solve():
                return True
            
            del assignment[literal]
            stack.pop()
            return False
        
        return len(stack) + 1
    
    def geometric_entropy(f):
        n = len(f)
        clauses = [f[i:i + n] for i in range(0, len(f), n)]
        count = sum(len(set(clause)) for clause in clauses)
        return math.log2(count)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            ge = geometric_entropy(f)
            t_f = dpll_refutation_size(f)
            if t_f == 0:
                continue
            results.append((ge / t_f, n))
    
    if not results:
        return {
            "metric_name": "GE/A",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ge_over_t_f = [r[0] for r in results]
    n_values = [r[1] for r in results]
    
    return {
        "metric_name": "GE/A",
        "metric_value": sum(ge_over_t_f) / len(ge_over_t_f),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(r[0] <= 2 for r in results),  # Assuming k = 1
        "counterexample": "" if all(r[0] <= 2 for r in results) else "GE/A > 2"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ge_over_t_f = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ge_over_t_f} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"GE/A > 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")