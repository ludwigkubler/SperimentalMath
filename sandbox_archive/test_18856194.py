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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def geometric_probability(clauses):
        n = len(clauses)
        total_length = sum(len(c) for c in clauses)
        if total_length == 0:
            return 0
        probability = (total_length / n) ** (1/3)
        return probability
    
    def upper_bound(n):
        return math.sqrt(3) * n ** (3/2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_probability = 0
        for _ in range(5):
            cnf = generate_cnf(n)
            prob = geometric_probability(cnf)
            upper = upper_bound(n)
            results.append((prob, upper))
            total_probability += prob
            instances_tested += 1
        
        mean_prob = total_probability / instances_tested
        mean_upper = sum(upper for _, upper in results) / len(results)
        
        if mean_prob > mean_upper:
            return {
                "metric_name": "geometric_probability",
                "metric_value": mean_prob,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mean_prob={mean_prob} > mean_upper={mean_upper}"
            }
    
    return {
        "metric_name": "geometric_probability",
        "metric_value": sum(prob for prob, _ in results) / len(results),
        "instances_tested": instances_tested * 6,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='geometric_probability' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")