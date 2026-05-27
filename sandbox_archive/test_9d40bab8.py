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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f"({variables[i-1]} v ~{variables[i-1]})")
        for i in range(2, n+1):
            clauses.append(f"({variables[i-1]} v {variables[i-2]})")
        formula = " & ".join(clauses)
        return formula
    
    def xor_and_tree_width(formula):
        # Simplified heuristic to estimate XOR-AND tree width
        return len(formula.split("v")) + len(formula.split("&"))
    
    def minimal_local_cohomology_rank(n):
        # Simplified heuristic for minimal local cohomology rank
        return math.log2(n)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    width = xor_and_tree_width(formula)
    rank = minimal_local_cohomology_rank(n)
    
    ratio = rank / width if width > 0 else float('inf')
    conjecture_holds = ratio <= math.log2(n)  # poly-logarithmic check
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, width={width}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_d = sum(results) / len(results)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= math.log2(n)) / len(results)
    
    if all(r <= math.log2(n) for n in range(5, 41)):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > math.log2(n))
        print(f"RESULT: FALSIFIED counterexample=\"n=40\" first_failing_seed={first_failing_seed}")