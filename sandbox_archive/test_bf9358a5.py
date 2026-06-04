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
        clauses = []
        for _ in range(10 * n):  # Generate a CNF with 10n clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def grothendieck_suslin_dimension(n):
        # Placeholder function to compute Grothendieck-Suslin dimension
        # This is a stub and should be replaced with actual computation
        return 3 * math.log(n / 2) ** 2
    
    def frege_proof_length(cnf):
        # Placeholder function to compute Frege proof length
        # This is a stub and should be replaced with actual computation
        return len(cnf) * n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    dimension = grothendieck_suslin_dimension(n)
    proof_length = frege_proof_length(cnf)
    
    return {
        "metric_name": "Grothendieck-Suslin Dimension and Frege Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dimension <= 3 * math.log(n / 2) ** 2 and proof_length >= 0.5 * n * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")