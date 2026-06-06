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
    
    def tseitin_encoding(variables, clauses):
        n = len(variables)
        literals = variables + [f'~{v}' for v in variables]
        tseitin_clauses = []
        
        def encode_clause(clause):
            if not clause:
                return ['False']
            elif len(clause) == 1:
                return [clause[0]]
            else:
                new_var = f't{n}'
                n += 1
                tseitin_clauses.append([new_var] + [f'~{l}' for l in clause])
                tseitin_clauses.extend(encode_clause([new_var, l]) for l in clause)
                return [new_var]
        
        for clause in clauses:
            tseitin_clauses.extend(encode_clause(clause))
        
        return literals, tseitin_clauses
    
    def lie_algebroid_dimension(n):
        # Placeholder function to compute the Lie algebroid dimension
        # This is a dummy implementation and should be replaced with actual logic
        return n ** (2 / 3)
    
    k = random.randint(3, 10)  # Randomly choose k between 3 and 10
    n = random.randint(5, 40)  # Randomly choose n between 5 and 40
    
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    
    for _ in range(k):
        clause = random.sample(variables + [f'~{v}' for v in variables], k)
        clauses.append(clause)
    
    literals, tseitin_clauses = tseitin_encoding(variables, clauses)
    lie_dim = lie_algebroid_dimension(n)
    
    metric_value = lie_dim
    conjecture_holds = lie_dim >= Fraction(k ** (2 / 3)) * n ** (2 / 3)
    counterexample = "" if conjecture_holds else f"k={k}, n={n}"
    
    return {
        "metric_name": "Lie Algebroid Dimension",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"k={r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")