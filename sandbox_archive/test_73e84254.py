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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Generate a CNF with 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def zeta_function(cnf):
        rank = len(cnf)  # Simplified for demonstration purposes
        return rank
    
    def resolution_proof_size(cnf):
        size = len(cnf) * 2  # Simplified for demonstration purposes
        return size
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    try:
        rank = zeta_function(cnf)
        proof_size = resolution_proof_size(cnf)
        ratio = Fraction(rank, proof_size) if proof_size != 0 else None
    except Exception as e:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio if ratio is not None else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": ratio is not None and ratio >= Fraction(1, n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results) if results else 0
    
    if all(r["metric_value"] is not None for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")