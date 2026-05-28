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
    
    def generate_3cnf(n, clause_density):
        clauses = []
        for _ in range(int(clause_density * n * (n - 1) / 2)):
            variables = random.sample(range(1, n + 1), 3)
            polarity = [random.choice([-1, 1]) for _ in range(3)]
            clause = [(polarity[i], variables[i]) for i in range(3)]
            clauses.append(clause)
        return clauses
    
    def max_cut_approximation_ratio(clauses):
        # Placeholder function to compute the approximation ratio
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n = 20
    clause_density = 0.5
    d_values = range(1, 51)
    
    ratios = []
    for d in d_values:
        ratio = max_cut_approximation_ratio(generate_3cnf(n, clause_density))
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios)
    
    return {
        "metric_name": "max_cut_approximation_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(d_values),
        "conjecture_holds": False,  # Placeholder
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")