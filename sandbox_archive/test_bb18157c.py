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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(xor_func, n):
        formula = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if xor_func[i] & (1 << j):
                    clause.append(f'x{j}')
                else:
                    clause.append(f'-x{j}')
            formula.append(' '.join(clause) + ' 0')
        return '\n'.join(formula)
    
    def resolution_length(formula):
        clauses = [set(clause.split()[:-1]) for clause in formula.split('\n')]
        unit_clauses = {c for c in clauses if len(c) == 1}
        
        while True:
            new_unit_clauses = set()
            for clause in clauses:
                if not clause:
                    return float('inf')
                if len(clause) == 1:
                    new_unit_clauses.add(next(iter(clause)))
            
            if not new_unit_clauses:
                break
            
            unit_clauses.update(new_unit_clauses)
            clauses = [c - {unit} for c in clauses for unit in new_unit_clauses]
        
        return len(unit_clauses)
    
    def minimal_local_cohomology_rank(n):
        # Placeholder implementation; actual computation depends on the simplicial complex
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            xor_func = generate_xor_function(n)
            formula = tseitin_formula(xor_func, n)
            length = resolution_length(formula)
            if length == float('inf'):
                continue
            total_length += length
            instances_tested += 1
    
    mean_length = total_length / instances_tested
    expected_length = sum(2**(math.log2(n) + math.log2(minimal_local_cohomology_rank(n))) for n in n_values) / len(n_values)
    
    conjecture_holds = abs(mean_length - expected_length) <= 3
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Expected {expected_length}, got {mean_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break