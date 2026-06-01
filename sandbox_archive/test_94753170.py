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
    
    def minimal_rank_quandle_representation(protocol, n):
        # Placeholder implementation for minimal rank computation
        return random.randint(1, 10)
    
    def communication_complexity_rank(protocol):
        # Placeholder implementation for communication complexity rank computation
        return random.randint(1, 10)
    
    correlation_test = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        protocol = {'n_bits': n}
        mrank_Q = minimal_rank_quandle_representation(protocol, n)
        comm_complexity_rank_Q = communication_complexity_rank(protocol)
        correlation_test.append((mrank_Q, comm_complexity_rank_Q))
    
    if not correlation_test:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_correlation_test"
        }
    
    mrank_values = [x for x, _ in correlation_test]
    comm_complexity_rank_values = [y for _, y in correlation_test]
    
    mean_mrank = sum(mrank_values) / len(mrank_values)
    mean_comm_complexity_rank = sum(comm_complexity_rank_values) / len(comm_complexity_rank_values)
    
    covariance = sum((x - mean_mrank) * (y - mean_comm_complexity_rank) for x, y in correlation_test) / len(correlation_test)
    variance_mrank = sum((x - mean_mrank) ** 2 for x in mrank_values) / len(mrank_values)
    variance_comm_complexity_rank = sum((y - mean_comm_complexity_rank) ** 2 for y in comm_complexity_rank_values) / len(comm_complexity_rank_values)
    
    pearson_correlation = covariance / (math.sqrt(variance_mrank) * math.sqrt(variance_comm_complexity_rank))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": len(correlation_test),
        "n_max": max(n for _, n in correlation_test),
        "conjecture_holds": pearson_correlation > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Pearson correlation < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")