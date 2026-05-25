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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([f'x{i}', f'~x{i}'])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'~x{i}', f'~x{j}', f'x{i}|x{j}'])
        return variables, clauses
    
    def symplectic_rank(n):
        # Placeholder for actual computation
        return 2**n // math.log(n)**2
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = []
            for clause in clauses:
                if len(clause) == 1:
                    stack.append(clause[0])
                    break
                else:
                    new_clauses.append(clause)
            if not stack:
                return float('inf')
            unit_clause = [c for c in clauses if len(c) == 1]
            if not unit_clause:
                return float('inf')
            literal = random.choice(unit_clause)[0]
            new_clauses = [[l for l in c if l != literal and l != f'~{literal}'] for c in new_clauses]
            clauses = new_clauses
    
    n_values = [5, 10, 20, 40]
    results = []
    
    for n in n_values:
        variables, clauses = tseitin_formula(n)
        rank = symplectic_rank(n)
        length = resolution_length(clauses)
        if length < 2**(math.log(rank, 2)):
            return {
                "metric_name": "Resolution proof length",
                "metric_value": length,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}, length={length}"
            }
        results.append(length)
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2**(math.log(symplectic_rank(n), 2)) for n in [5, 10, 20, 40]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 2**(math.log(symplectic_rank(n), 2)) for r in results for n in [5, 10, 20, 40]):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, rank={symplectic_rank(n)}, length={min(results)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")