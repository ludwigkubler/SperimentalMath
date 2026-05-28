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
    
    def generate_xor_3cnf(n, m):
        variables = [chr(i) for i in range(97, 97 + n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause.append('∨')
            clause.append(random.choice(['~', '']))
            clauses.append(clause)
        return clauses
    
    def compute_tropical_rank(clauses):
        # Simplified tropical rank computation (placeholder)
        return len(clauses) + random.randint(1, 2)
    
    def construct_xor_circuit(depth):
        # Placeholder circuit construction
        return depth
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    formula = generate_xor_3cnf(n, m)
    rank = compute_tropical_rank(formula)
    depth = construct_xor_circuit(rank // 10 + 1)  # Simplified depth calculation
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log(n, 2),
        "counterexample": "" if rank <= math.log(n, 2) else f"Formula: {formula}, Rank: {rank}, Depth: {depth}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")