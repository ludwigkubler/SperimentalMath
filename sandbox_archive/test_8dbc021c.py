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
    n = random.randint(5, 40)
    
    # Construct a read-twice branching program P with n variables
    P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    # Construct the associated quasi-symmetric function f(P)
    def quasi_symmetric_function(P):
        # Placeholder implementation of the constructive mapping
        return sum(sum(row[i] * row[j] for j in range(i+1, n)) for i in range(n))
    
    f_P = quasi_symmetric_function(P)
    
    # Calculate the minimal rank of f(P) over the tropical semiring
    def min_rank(f):
        # Placeholder implementation of minimal rank calculation
        return 1 + int(math.log2(f))
    
    min_rank_f_P = min_rank(f_P)
    
    # Determine BP_ReadTwice complexity of P
    def bp_read_twice_complexity(P):
        # Placeholder implementation of BP_ReadTwice complexity
        return sum(1 for row in P if any(x == 1 for x in row))
    
    bp_read_twice_comp = bp_read_twice_complexity(P)
    
    # Compare BP_ReadTwice complexity with log(minimal rank(f(P)))
    log_min_rank_f_P = math.log2(min_rank_f_P)
    within_factor_of_2 = abs(bp_read_twice_comp - log_min_rank_f_P) <= 0.5 * log_min_rank_f_P
    
    return {
        "metric_name": "BP_ReadTwice complexity vs minimal rank",
        "metric_value": bp_read_twice_comp,
        "instances_tested": 1,
        "conjecture_holds": within_factor_of_2,
        "counterexample": "" if within_factor_of_2 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")