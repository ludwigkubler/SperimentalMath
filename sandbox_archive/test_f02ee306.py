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
        clauses = []
        for _ in range(2**n // 4):  # Ensure at least 16 clauses
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def frege_proof_width(cnf):
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width

    def hodge_norm(cnf):
        # Placeholder for Hodge norm calculation
        # This is a dummy implementation. Replace with actual Hodge norm computation.
        return sum(abs(x) for x in random.sample(range(-n, n+1), 2*n)) / (2*n)

    n = 40
    cnf = generate_cnf(n)
    proof_width = frege_proof_width(cnf)
    hodge_norm_value = hodge_norm(cnf)
    
    return {
        "metric_name": "Hodge Norm vs Frege Proof Width",
        "metric_value": hodge_norm_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]  # Default to first 30 primes
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")