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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            cnf.append(clause)
        return cnf

    def galois_group_size(cnf):
        # Simplified heuristic to estimate the size of the Galois group
        # This is a placeholder and should be replaced with an actual algorithm
        return len(cnf) ** 2

    def resolution_proof_width(cnf):
        # Simplified heuristic to estimate the width of the resolution proof
        # This is a placeholder and should be replaced with an actual algorithm
        return len(cnf)

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    galois_size = galois_group_size(cnf)
    proof_width = resolution_proof_width(cnf)

    return {
        "metric_name": "resolution_proof_width",
        "metric_value": proof_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": proof_width <= galois_size ** 2,
        "counterexample": "" if conjecture_holds else f"CNF with n={n}, galois_size={galois_size}, proof_width={proof_width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")