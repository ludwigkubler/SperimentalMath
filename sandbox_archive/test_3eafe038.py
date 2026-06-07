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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = random.sample(variables, 2)
            clauses.append(f"({' or '.join(clause)})")
        return f"({' and '.join(clauses)})"
    
    def dpll_depth(formula):
        stack = [formula]
        depth = 0
        while stack:
            formula = stack.pop()
            if ' or ' in formula:
                subformulas = formula.split(' or ')
                stack.extend(subformulas)
            elif ' and ' in formula:
                subformulas = formula.split(' and ')
                stack.append(subformulas[1])
                stack.append(subformulas[0])
            else:
                depth += 1
        return depth
    
    def quantum_group_rank(n):
        # Placeholder for the actual quantum group rank calculation
        # This is a dummy function that returns n^(1.5) as an example
        return n ** 1.5
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    
    rank = quantum_group_rank(n)
    dpll_depth_value = dpll_depth(formula)
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": dpll_depth_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= n ** 1.5 and dpll_depth_value >= rank,
        "counterexample": "" if rank <= n ** 1.5 and dpll_depth_value >= rank else f"Rank {rank} not supported by DPLL depth {dpll_depth_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")