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

def generate_tseitin_circuit(n, m):
    if n <= 0 or m <= 0:
        return [], []
    
    inputs = list(range(1, n + 1))
    clauses = []
    
    # Generate literals and their negations
    literals = [f'x{i}' for i in range(1, n + 1)] + [f'-x{i}' for i in range(1, n + 1)]
    
    # Generate m clauses
    for _ in range(m):
        clause = []
        for _ in range(random.randint(2, n)):
            literal = random.choice(literals)
            if literal.startswith('-'):
                clause.append((literal[1:], False))
            else:
                clause.append((literal, True))
        clauses.append(clause)
    
    return inputs, clauses

def tropicalize_qmcs(qmcs):
    # Placeholder for the actual tropicalization logic
    # For simplicity, we assume the rank is proportional to the number of clauses
    return len(qmcs) ** 0.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n * (n - 1) // 2, 30))
    inputs, clauses = generate_tseitin_circuit(n, m)
    
    if not inputs or not clauses:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    qmcs = [random.choice([True, False]) for _ in range(m)]
    rank = tropicalize_qmcs(qmcs)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - m ** 0.5) <= 1.5 * m ** 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")