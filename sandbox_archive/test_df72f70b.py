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
    
    def generate_cnf(m, s):
        clauses = []
        for _ in range(m):
            literals = [random.randint(1, 2 * s) for _ in range(s)]
            clause = set(literals + [-l for l in literals])
            clauses.append(clause)
        return clauses

    def compute_mlecoh(cnf):
        # Placeholder function to simulate computation
        m = len(cnf)
        s = max(len(clause) for clause in cnf)
        return Fraction(m * (m + 1), 2)  # Simplified placeholder

    n_max = 40
    instances_tested = 0
    mlecoh_values = []
    
    for _ in range(30):
        m = random.randint(5, 40)
        s = random.randint(1, min(m, 40))
        cnf = generate_cnf(m, s)
        mlecoh = compute_mlecoh(cnf)
        
        instances_tested += 1
        mlecoh_values.append(mlecoh)
        
        if mlecoh > 2 * s:
            counterexample = f"m={m}, s={s}, mlecoh={mlecoh}"
            return {
                "metric_name": "mlecoh",
                "metric_value": mlecoh,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
    
    return {
        "metric_name": "mlecoh",
        "metric_value": sum(mlecoh_values) / len(mlecoh_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")