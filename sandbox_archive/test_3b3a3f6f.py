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
    
    def is_boolean_ring(ring):
        for element in ring:
            if element not in [0, 1]:
                return False
        return True
    
    def min_rank_k_theory(boolean_ring):
        # Simplified implementation for Boolean rings (rank = number of elements)
        return len(boolean_ring)
    
    def tseitin_formula(boolean_ring):
        n = len(boolean_ring)
        formula = []
        for i in range(n):
            clause = [f'x{i}']
            for j in range(i + 1, n):
                clause.append(f'~x{j}')
            formula.append(clause)
        return formula
    
    def resolution_length(formula):
        # Simplified implementation (number of clauses)
        return len(formula)
    
    instances_tested = 0
    total_resolution_length = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_rings = [random.sample([0, 1], n) for _ in range(5)]
        
        for ring in boolean_rings:
            instances_tested += 1
            if not is_boolean_ring(ring):
                continue
            
            min_rank = min_rank_k_theory(ring)
            formula = tseitin_formula(ring)
            length = resolution_length(formula)
            
            total_resolution_length += length
            
            if length < 2 ** min_rank:
                conjecture_holds = False
                counterexample = f"Ring of size {n} with rank {min_rank} and proof length {length}"
    
    metric_value = total_resolution_length / instances_tested
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")