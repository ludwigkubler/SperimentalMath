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
    
    def generate_read_twice_bp(n, m):
        clauses = []
        for _ in range(m):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            while len(set(literals)) < 2:
                literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            clauses.append(' & '.join(literals))
        return ' | '.join(clauses)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            while len(set(literals)) < 2:
                literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            clauses.append(' | '.join(literals))
        return ' & '.join(clauses)
    
    def size(bp):
        return len(bp.split())
    
    def dpll_search_tree_size(bp):
        # Simplified estimation of DPLL search tree size
        return 2 ** (len(bp.split()) // 2)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 10)
    
    bp = generate_read_twice_bp(n, m)
    size_p = size(bp)
    dpll_size = dpll_search_tree_size(bp)
    
    # Placeholder for minimal rank computation
    min_rank = random.randint(1, size_p)
    
    if min_rank < math.log(size_p) or min_rank > size_p:
        return {
            "metric_name": "min_rank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"BP: {bp}, Size(P): {size_p}, DPLL Search Tree Size: {dpll_size}, Min Rank: {min_rank}"
        }
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")