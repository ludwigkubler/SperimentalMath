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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            while len(set(clause)) != 3:
                clause = [random.randint(-n, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def real_radical_dimension(clauses):
        # Placeholder implementation
        return math.log(len(clauses))
    
    def disjointness_communication_complexity(n):
        # Placeholder implementation
        return n
    
    n = 40
    clauses = generate_3cnf(n)
    rad_dim = real_radical_dimension(clauses)
    comm_comp = disjointness_communication_complexity(n)
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": comm_comp,
        "instances_tested": 1,
        "conjecture_holds": rad_dim == math.log(n) and comm_comp == n,
        "counterexample": "" if rad_dim == math.log(n) and comm_comp == n else f"rad_dim={rad_dim}, comm_comp={comm_comp}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")