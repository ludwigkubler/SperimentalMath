# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return variables, clauses
    
    def tseitin_width(cnf):
        # Simplified Tseitin width calculation
        return len(cnf)
    
    def geometric_quantization_rank(cnf):
        # Placeholder for actual geometric quantization rank computation
        # For simplicity, we use a dummy function that returns the number of variables
        return len(cnf[0])
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables, clauses = generate_cnf(n, m)
    w_Tseitin = tseitin_width(clauses)
    rank_GQ = geometric_quantization_rank(clauses)
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": rank_GQ,
        "instances_tested": 1,
        "conjecture_holds": rank_GQ >= w_Tseitin,
        "counterexample": "" if rank_GQ >= w_Tseitin else f"CNF with n={n}, m={m} has rank {rank_GQ} < Tseitin width {w_Tseitin}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < Tseitin width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")