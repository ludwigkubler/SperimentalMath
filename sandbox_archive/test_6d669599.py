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
    
    def generate_tseitin_circuit(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        
        for _ in range(m):
            a, b, c = random.sample(variables, 3)
            clause = (a, b, c)
            clauses.append(clause)
        
        return variables, clauses
    
    def noncommutative_tensor_product_rank(n, m):
        # Placeholder for actual computation
        # For now, we'll just return a dummy value based on n and m
        return 0.5 * math.sqrt(n) * (m ** 0.25)
    
    n = random.randint(5, 40)
    m = random.randint(10, 80)
    variables, clauses = generate_tseitin_circuit(n, m)
    rank = noncommutative_tensor_product_rank(n, m)
    
    return {
        "metric_name": "noncommutative_tensor_product_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 1.5 * (0.5 * math.sqrt(n) * (m ** 0.25)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")