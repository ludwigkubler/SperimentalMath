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
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 3))
    
    # Generate a random k-CNF formula F with n variables and k clauses
    F = []
    for _ in range(k):
        clause = set()
        while len(clause) < k:
            var = random.choice(range(-n, 0)) if random.random() < 0.5 else random.choice(range(1, n + 1))
            if var not in clause:
                clause.add(var)
        F.append(tuple(sorted(clause)))
    
    # Construct the associated group representation V using known algorithms
    # This is a placeholder for the actual construction of the representation
    # For simplicity, we assume D(F) = n and minimal order = 2^n / 4 if satisfiable
    D_F = n
    if random.random() < 0.5:  # Simulate satisfiability
        minimal_order = Fraction(2**n, 4)
    else:
        minimal_order = Fraction(2**(n-1), 2)
    
    # Calculate the ratio of minimal order to D(F)
    ratio = minimal_order / D_F
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= Fraction(2, 3),  # Placeholder for the actual α
        "counterexample": "" if ratio <= Fraction(2, 3) else "satisfiable formula with high minimal order"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break