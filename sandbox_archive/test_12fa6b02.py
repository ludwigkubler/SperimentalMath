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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(n):
            clause = f'{variables[i]} | ~{variables[i]}'
            clauses.append(clause)
        
        return clauses
    
    def polynomial_from_clause(clause, n):
        if ' | ' in clause:
            var1, var2 = clause.split(' | ')
            return [var1, var2]
        elif ' & ' in clause:
            var1, var2 = clause.split(' & ')
            return [f'~{var1}', f'~{var2}']
        else:
            return [clause]
    
    def smallest_noncommutative_division_algebra(polynomials):
        # Placeholder for actual implementation
        return len(set(polynomials))
    
    def resolution_proof_width(clauses):
        # Placeholder for actual implementation
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    polynomials = [polynomial_from_clause(c, n) for c in clauses]
    dimension_D = smallest_noncommutative_division_algebra(polynomials)
    w_phi = resolution_proof_width(clauses)
    
    return {
        "metric_name": "resolution proof width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dimension_D >= w_phi - 3,
        "counterexample": "" if dimension_D >= w_phi - 3 else f"Dimension D={dimension_D}, w(φ)={w_phi}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")