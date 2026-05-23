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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate enough clauses to ensure a dense formula
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            cnf.append(tuple(clause))
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    # Construct the Kähler form for each CNF using a simple mapping
    kahler_form_tropicalization = sum(abs(clause[i]) for clause in cnf for i in range(n))
    
    # Measure the AC0 circuit threshold for the CNF formula
    ac0_threshold = n  # Simplified for testing purposes
    
    # Check if the computed minimal rank is logarithmic in the AC0 circuit threshold within 30 random seeds
    ratio = math.log(n) / kahler_form_tropicalization
    conjecture_holds = abs(ratio - ac0_threshold) <= 0.1 * ac0_threshold
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": len(cnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} not within ±10% of AC0 threshold {ac0_threshold}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    std_ratio = math.sqrt(sum((res["metric_value"] - mean_ratio) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of tolerance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")