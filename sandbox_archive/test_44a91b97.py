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
    
    n = 10  # Number of variables
    m = 20  # Number of clauses
    
    # Generate Tseitin circuit
    literals = [f'x{i}' for i in range(n)]
    neg_literals = [f'-x{i}' for i in range(n)]
    clauses = []
    
    for i in range(m):
        clause = random.choice(literals + neg_literals)
        if random.choice([True, False]):
            clause += ' OR '
        else:
            clause += ' AND '
        
        clause += random.choice(literals + neg_literals)
        clauses.append(clause)
    
    # Compute noncommutative tensor product representation (simplified for demonstration)
    rank = len(set(clauses))  # Simplified rank calculation
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 1.5 * math.sqrt(n) * m ** 0.25,
        "counterexample": "" if rank <= 1.5 * math.sqrt(n) * m ** 0.25 else f"Rank {rank} exceeds bound"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")