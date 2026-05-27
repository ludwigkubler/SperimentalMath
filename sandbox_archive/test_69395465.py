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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_refutation_depth(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a boolean function of n variables")
        
        def dpll(state, literals):
            if not literals:
                return all(f[i] == state[i] for i in range(n))
            
            literal = literals[0]
            pos_literal = literal
            neg_literal = -literal
            
            if any(f[i] == pos_literal for i in range(n)):
                if dpll(state, literals[1:]):
                    return True
            
            if any(f[i] == neg_literal for i in range(n)):
                if dpll(state + [neg_literal], literals[1:]):
                    return True
            
            return False
        
        depth = 0
        stack = [([], list(range(1, n+1)))]
        while stack:
            state, literals = stack.pop()
            if not literals:
                continue
            literal = literals[0]
            pos_literal = literal
            neg_literal = -literal
            
            if any(f[i] == pos_literal for i in range(n)):
                stack.append((state + [pos_literal], literals[1:]))
                depth += 1
                continue
            
            if any(f[i] == neg_literal for i in range(n)):
                stack.append((state + [neg_literal], literals[1:]))
                depth += 1
                continue
        
        return depth
    
    def quasi_linear_representation(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a boolean function of n variables")
        
        # Simplified representation for demonstration purposes
        return sum(f[i] * (1 << i) for i in range(n))
    
    def linear_equivalence(r1, r2):
        return r1 == r2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    depth = dpll_refutation_depth(f)
    rank = quasi_linear_representation(f)
    
    if depth == 0 or rank == 0:
        return {
            "metric_name": "rho/f",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "depth or rank is zero"
        }
    
    ratio = rank / depth
    
    return {
        "metric_name": "rho/f",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_rho_f = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho_f} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_counterexample = next(r for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample['counterexample']}\" first_failing_seed={first_counterexample['seed']}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")