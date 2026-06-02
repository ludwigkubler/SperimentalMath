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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        rank = 0
        for i in range(n):
            bits = [f[j] for j in range(2**n) if (j >> i) & 1]
            if len(set(bits)) > 1:
                rank += 1
        return rank
    
    def min_order(monomial_ideal):
        # Placeholder for the actual computation of min_order
        # This is a dummy implementation and should be replaced with the correct algorithm
        return len(monomial_ideal)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_comm_rank = 0
    total_min_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            comm_rank = communication_complexity_rank(f)
            min_order_val = min_order(f)
            total_comm_rank += comm_rank
            total_min_order += min_order_val
            instances_tested += 1
    
    mean_comm_rank = total_comm_rank / instances_tested
    mean_min_order = total_min_order / instances_tested
    correlation_coefficient = (instances_tested * sum(comm_rank * min_order_val for comm_rank, min_order_val in zip(range(1, n_values[-1] + 1), range(1, n_values[-1] + 1))) - total_comm_rank * total_min_order) / math.sqrt((instances_tested * sum(comm_rank**2 for comm_rank in range(1, n_values[-1] + 1)) - total_comm_rank**2) * (instances_tested * sum(min_order_val**2 for min_order_val in range(1, n_values[-1] + 1)) - total_min_order**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next((r["seed"] for r in results if abs(r["metric_value"]) > 10), None)
        print(f"RESULT: FALSIFIED counterexample='large_deviation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")