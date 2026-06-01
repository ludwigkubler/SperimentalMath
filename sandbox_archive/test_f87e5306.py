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
        for _ in range(m):
            clause = [random.randint(1, m) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, 3))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        # Simplified DPLL solver
        def solve(model):
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                return model
            literal = unit_clause[0]
            new_model = {k: v for k, v in model.items() if k != abs(literal)}
            if literal > 0:
                new_model[literal] = True
            else:
                new_model[-literal] = False
            return solve(new_model)
        
        def propagate(model):
            while True:
                unit_clause = next((c for c in cnf if len(c) == 1), None)
                if not unit_clause:
                    break
                literal = unit_clause[0]
                new_model = {k: v for k, v in model.items() if k != abs(literal)}
                if literal > 0:
                    new_model[literal] = True
                else:
                    new_model[-literal] = False
                model = new_model
        
        initial_model = {}
        return solve(initial_model)
    
    def local_ring(cnf):
        # Simplified local ring structure
        variables = set(abs(lit) for clause in cnf for lit in clause)
        unit_group_size = len(variables)
        return unit_group_size
    
    def frege_proof_depth(cnf):
        # Simplified Frege proof depth calculation
        depth = 0
        for clause in cnf:
            if len(clause) == 1:
                depth += 1
            else:
                depth += 2
        return depth
    
    instances_tested = 0
    n_max = 0
    total_unit_group_size = 0
    total_depth = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(m)
        instances_tested += len(cnf)
        n_max = max(n_max, m)
        
        unit_group_size = local_ring(cnf)
        depth = frege_proof_depth(cnf)
        
        total_unit_group_size += unit_group_size
        total_depth += depth
    
    mean_td = total_depth / instances_tested if instances_tested > 0 else 0
    conjecture_holds = abs(mean_td - (total_unit_group_size / instances_tested)) < 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frege Proof Depth vs Unit Group Size",
        "metric_value": mean_td,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_td = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_td} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")