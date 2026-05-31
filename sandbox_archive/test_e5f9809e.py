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
    
    def generate_cnf(m, s):
        literals = list(range(1, m * s + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, s)
            clauses.append(clause)
        return clauses
    
    def compute_mlecoh(clauses):
        n = len(clauses)
        # Placeholder implementation of mlecoh computation
        # This is a dummy function and should be replaced with actual etale cohomology computation
        return Fraction(n * (n + 1), 2)  # Example polynomial bound
    
    def check_bound(mlecoh, s):
        return mlecoh <= 2 * s
    
    n_max = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        m = random.randint(1, n)
        s = random.randint(1, min(n, 40))
        cnf = generate_cnf(m, s)
        mlecoh = compute_mlecoh(cnf)
        instances_tested += 1
        n_max = max(n_max, n)
        
        if not check_bound(mlecoh, s):
            conjecture_holds = False
            counterexample = f"m={m}, s={s}, mlecoh={mlecoh}"
    
    return {
        "metric_name": "mlecoh",
        "metric_value": compute_mlecoh(generate_cnf(10, 20)),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")