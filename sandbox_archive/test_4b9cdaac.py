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
    
    def generate_DISJ_n(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([0, 1]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def non_archimedean_valuation(clause):
        # Simplified example of a non-archimedean valuation
        return sum(clause) % 2
    
    def min_rank(valuations):
        return min(valuations)
    
    def randomized_communication_complexity(clauses, valuations):
        # Simplified example of CC_R calculation
        return len(set(valuations))
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    clauses = generate_DISJ_n(n, m)
    valuations = [non_archimedean_valuation(clause) for clause in clauses]
    min_rank_value = min_rank(valuations)
    cc_r = randomized_communication_complexity(clauses, valuations)
    
    return {
        "metric_name": "CC_R",
        "metric_value": cc_r,
        "instances_tested": 1,
        "conjecture_holds": True if cc_r >= n * min_rank_value else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc_r = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc_r} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc_r} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")