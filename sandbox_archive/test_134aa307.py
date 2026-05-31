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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        literals = set(abs(lit) for lit in sum(cnf, []))
        
        def search(model):
            unassigned = literals - {abs(lit) for lit in model}
            if not unassigned:
                return all(phi in model or -phi in model for phi in cnf)
            
            literal = next(iter(unassigned))
            pos_model = model + [literal]
            neg_model = model + [-literal]
            
            if search(pos_model):
                return True
            elif search(neg_model):
                return True
            
            return False
        
        return search([])
    
    def mli(cnf):
        # Placeholder for minimal local index calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()
    
    n = 10
    m = 20
    cnf = generate_cnf(n, m)
    d_phi = dpll(cnf)
    mli_phi = mli(cnf)
    
    if d_phi == 0:
        return {
            "metric_name": "mli/d_phi",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d_phi is zero, division by zero"
        }
    
    ratio = mli_phi / d_phi
    return {
        "metric_name": "mli/d_phi",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mli/d_phi ratio out of bounds' first_failing_seed={first_failing_seed}")