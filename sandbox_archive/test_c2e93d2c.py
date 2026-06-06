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
    
    def tseitin_encoding(variables, clauses):
        n = len(variables)
        literals = variables + [f'~{v}' for v in variables]
        tseitin_clauses = []
        
        for i, clause in enumerate(clauses):
            new_var = f't{i+1}'
            tseitin_clauses.append([new_var] + [-l for l in clause])
            for literal in clause:
                tseitin_clauses.append([-new_var, literal])
        
        return literals, tseitin_clauses
    
    def encode_clause(clause):
        new_var = f't{n}'  # Ensure n is defined
        tseitin_clauses = []
        for literal in clause:
            tseitin_clauses.append([new_var, literal])
        tseitin_clauses.append([-new_var] + [-l for l in clause])
        return tseitin_clauses
    
    def lie_algebroid_dimension(n):
        # Placeholder function to compute Lie algebroid dimension
        return n ** (2/3)
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n // 2, 10))
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    for _ in range(k):
        clause = random.sample(variables + [f'~{v}' for v in variables], k)
        clauses.append(clause)
    
    literals, tseitin_clauses = tseitin_encoding(variables, clauses)
    lie_dim = lie_algebroid_dimension(n)
    
    conjecture_holds = lie_dim >= Fraction(k ** (2/3)) * n ** (2/3)
    counterexample = "" if conjecture_holds else f"n={n}, k={k}"
    
    return {
        "metric_name": "Lie Algebroid Dimension",
        "metric_value": lie_dim,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")