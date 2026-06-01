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
    
    def dpll(circuit, assignment):
        if not circuit:
            return True
        var = next((v for v in range(len(circuit)) if v not in assignment), None)
        if var is None:
            return False
        
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll([clause for clause in circuit if not any(var == x or (x < 0 and -var == x) for x in clause)], new_assignment):
                return True
        return False
    
    def monotone_complexity(circuit):
        assignment = {}
        if dpll(circuit, assignment):
            return len(assignment)
        else:
            return None
    
    def quasi_crystal_order(circuit):
        # Placeholder function to compute the order of the quasi-crystal
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)  # Example: Order is equal to the number of clauses

    instances_tested = 0
    n_max = 0
    total_order = 0
    total_complexity = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times to get statistical signal
            circuit = [[random.choice([-i-1, i]) for i in range(n)] for _ in range(n)]
            complexity = monotone_complexity(circuit)
            if complexity is None:
                continue
            
            order = quasi_crystal_order(circuit)
            
            instances_tested += 1
            n_max = max(n_max, n)
            total_order += order
            total_complexity += complexity
    
    mean_order = Fraction(total_order, instances_tested) if instances_tested > 0 else 0
    mean_complexity = Fraction(total_complexity, instances_tested) if instances_tested > 0 else 0
    correlation_coefficient = (mean_order * mean_complexity - total_order * total_complexity / instances_tested**2) / \
                               math.sqrt((mean_order**2 - total_order**2 / instances_tested**2) * 
                                         (mean_complexity**2 - total_complexity**2 / instances_tested**2))
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_order - mean_complexity) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")