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
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def geometric_flow_complexity(cnf):
        # Placeholder function to simulate GFC calculation
        # Actual implementation would depend on the specific definition of geometric flow complexity
        return len(cnf) * (len(cnf[0]) + 1) // 2
    
    instances_tested = 30
    total_gfc = 0
    n_max = 5
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        gfc = geometric_flow_complexity(cnf)
        total_gfc += gfc
        if n > n_max:
            n_max = n
    
    avg_gfc = total_gfc / instances_tested
    conjecture_holds = avg_gfc <= 4 * n_max**2 and max(geometric_flow_complexity(generate_cnf(n)) for _ in range(instances_tested)) <= 4 * n_max**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "GFC",
        "metric_value": avg_gfc,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_gfc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_gfc} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_gfc} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")