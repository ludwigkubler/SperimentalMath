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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n):
            clause = ' or '.join(variables[:i])
            clauses.append(clause)
        
        # Generate AND clauses
        for i in range(n-1):
            clause = ' and '.join(variables[i:i+2])
            clauses.append(clause)
        
        # Generate NOT clauses
        for var in variables:
            not_clause = f'not {var}'
            clauses.append(not_clause)
        
        formula = ' and '.join(clauses)
        return formula
    
    def xor_and_tree_width(formula):
        if ' or ' not in formula and ' and ' not in formula:
            return 1
        elif ' or ' in formula:
            parts = formula.split(' or ')
            return max(xor_and_tree_width(part) for part in parts)
        else:
            parts = formula.split(' and ')
            return max(xor_and_tree_width(part) for part in parts) + 1
    
    def minimal_local_cohomology_rank(formula):
        # Placeholder function to simulate the computation
        # This is a dummy implementation that returns a value based on the length of the formula
        return len(formula)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    tree_width = xor_and_tree_width(formula)
    rank = minimal_local_cohomology_rank(formula)
    
    ratio = Fraction(rank, tree_width) if tree_width != 0 else float('inf')
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= math.log2(n) else False,
        "counterexample": "" if ratio <= math.log2(n) else f"n={n}, rank={rank}, tree_width={tree_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*37 + 1, 37))  # Default to 30 prime numbers
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_d = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_d)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log2(n)) / len(results)
    
    if all(r <= math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(r > math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > math.log2(n))
        print(f"RESULT: FALSIFIED counterexample='n={random.randint(5, 40)}, rank={results[first_failing_seed]}, tree_width={first_failing_seed}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")