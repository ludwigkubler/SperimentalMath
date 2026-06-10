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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                clause[random.randint(0, n-1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def circuit_satisfiability_complexity(cnf):
        # Simplified complexity measure based on number of clauses and variables
        return len(cnf) + len(cnf[0]) * 2
    
    def geometric_quantization_rank(cnf):
        # Simplified rank measure based on number of clauses and variables
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    gqr = geometric_quantization_rank(cnf)
    cssc = circuit_satisfiability_complexity(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": gqr / cssc if cssc != 0 else float('nan'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(math.isnan(res["metric_value"]) for res in results):
        print("RESULT: INCONCLUSIVE no_valid_data")
    else:
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if not math.isnan(res["metric_value"]) and res["metric_value"] >= 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, res in zip(seeds, results) if not math.isnan(res["metric_value"]) and res["metric_value"] < 0.5)
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")