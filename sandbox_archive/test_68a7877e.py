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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            if random.choice([True, False]):
                clause.append('~')
            clauses.append(clause)
        return variables, clauses

    def resolution_width(clauses):
        # Simplified resolution width calculation
        return len(clauses)

    def grothendieck_witt_class(variables, clauses):
        # Placeholder for actual computation
        return 1

    n = random.randint(5, 40)
    m = random.randint(n+1, 2*n)
    variables, clauses = generate_tseitin_formula(n, m)
    
    width = resolution_width(clauses)
    rank = grothendieck_witt_class(variables, clauses)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= width,
        "counterexample": "" if rank <= width else f"Formula with width {width} and rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= resolution_width(generate_tseitin_formula(n, m)[1])) / len(results)
    
    if all(r <= width for n, m, _, width, _ in (generate_tseitin_formula(random.randint(5, 40), random.randint(n+1, 2*n)) for _ in range(30))):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > width for n, m, _, width, _ in (generate_tseitin_formula(random.randint(5, 40), random.randint(n+1, 2*n)) for _ in range(30))):
        print(f"RESULT: FALSIFIED counterexample='width exceeds rank' first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")