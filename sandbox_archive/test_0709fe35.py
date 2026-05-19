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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def is_sat(instance):
        assignment = {i: random.choice([True, False]) for i in range(1, len(instance[0]) + 1)}
        for clause in instance:
            if all(assignment[var] == (val > 0) for var, val in zip(clause, clause)):
                return True
        return False
    
    def betti_number_complexity(n):
        # Placeholder function to compute Betti numbers
        # This is a dummy implementation and should be replaced with actual computation
        return n
    
    def sos_rank(instance):
        # Placeholder function to compute SOS rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(instance)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_3sat_instance(n)
    betti_sum = sum(betti_number_complexity(len(instance)))
    sos_rank_value = sos_rank(instance)
    
    metric_name = "Betti Sum vs SOS Rank"
    metric_value = betti_sum
    instances_tested = 1
    conjecture_holds = betti_sum <= sos_rank_value
    counterexample = "" if conjecture_holds else f"n={n}, Betti Sum={betti_sum}, SOS Rank={sos_rank_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")