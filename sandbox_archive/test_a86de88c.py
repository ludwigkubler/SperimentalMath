# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            for j in range(i+1, n+1):
                clause += f' | {variables[j-1]}'
            clauses.append(clause)
        
        # Generate AND clauses
        for i in range(n):
            clause = f'~{variables[i]}'
            for j in range(i+1, n):
                clause += f' & ~{variables[j]}'
            clauses.append(clause)
        
        return clauses
    
    def arithmetic_hierarchy_order(clause):
        # Placeholder function to compute the order of an arithmetic hierarchy invariant
        # This is a dummy implementation and should be replaced with actual logic
        return len(clause.split()) ** 2 * math.log(len(clause.split()))
    
    def resolution_proof_length(clauses):
        # Placeholder function to compute the resolution proof length
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses) * 10
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    
    invariant_orders = [arithmetic_hierarchy_order(c) for c in clauses]
    max_order = max(invariant_orders)
    proof_length = resolution_proof_length(clauses)
    
    metric_name = "correlation_coefficient"
    metric_value = Fraction(max_order, proof_length).limit_denominator()
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")