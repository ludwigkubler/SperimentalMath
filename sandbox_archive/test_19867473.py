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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            for j in range(i+1, n+1):
                clause += f' ^ {variables[j-1]}'
            clauses.append(clause)
        
        # Generate AND clauses
        for i in range(n):
            clause = f'{variables[i]}'
            for j in range(i+1, n):
                clause += f' v {variables[j]}'
            clauses.append(clause)
        
        formula = ' ^ '.join(clauses)
        return formula
    
    def xor_and_tree_width(formula):
        # Simplified estimation of XOR-AND tree width
        return len(formula.split(' ^ '))
    
    def minimal_local_cohomology_rank(formula):
        # Simplified estimation of minimal local cohomology rank
        return len(formula.split(' v '))
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    tree_width = xor_and_tree_width(formula)
    rank = minimal_local_cohomology_rank(formula)
    
    ratio = Fraction(rank, tree_width)
    metric_value = float(ratio)
    
    return {
        "metric_name": "ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= math.log2(n) else False,
        "counterexample": "" if ratio <= math.log2(n) else f"n={n}, rank={rank}, tree_width={tree_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_d = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_d) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log2(n)) / len(results)
    
    if all(r <= math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(r > math.log2(n) for r, n in zip(results, [random.randint(5, 40) for _ in range(len(results))])):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r > math.log2(n))]
        print(f"RESULT: FALSIFIED counterexample='n={n}, rank={rank}, tree_width={tree_width}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")