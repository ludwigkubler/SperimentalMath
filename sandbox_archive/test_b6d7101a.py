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

# Constants
MAX_N = 40
NUM_INSTANCES_PER_SEED = 30
CONJECTURE_SUPPORT_THRESHOLD = 0.8
CONSTANT_MULTIPLE = 1.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def calculate_comm_rank(protocol):
        return sum(p) / len(p)
    
    def calculate_comm_rank_var(protocol):
        comm_ranks = [calculate_comm_rank(p) for p in protocol]
        mean = sum(comm_ranks) / len(comm_ranks)
        var = sum((x - mean) ** 2 for x in comm_ranks) / len(comm_ranks)
        return var
    
    def run_protocol(n):
        # Generate a random n-communication protocol
        protocol = [[random.randint(1, 10) for _ in range(n)] for _ in range(NUM_INSTANCES_PER_SEED)]
        lid = sum(p[0] for p in protocol) / len(protocol)
        comm_rank_var = calculate_comm_rank_var(protocol)
        return lid, comm_rank_var
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        lid, comm_rank_var = run_protocol(n)
        results.append({
            "n": n,
            "lid": lid,
            "comm_rank_var": comm_rank_var
        })
    
    mean_lid = sum(result["lid"] for result in results) / len(results)
    std_lid = math.sqrt(sum((result["lid"] - mean_lid) ** 2 for result in results) / len(results))
    
    correlation_coefficient = sum((result["lid"] - mean_lid) * (result["comm_rank_var"] - mean_comm_rank_var) 
                                  for result in results) / (len(results) * std_lid * mean_comm_rank_var)
    
    if correlation_coefficient < CONJECTURE_SUPPORT_THRESHOLD:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Correlation coefficient is below threshold"
        }
    
    if any(result["lid"] > CONSTANT_MULTIPLE * mean_comm_rank_var + 3 * std_lid for result in results):
        return {
            "metric_name": "lid_bound",
            "metric_value": max(result["lid"] for result in results),
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "LID exceeds bound"
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= CONJECTURE_SUPPORT_THRESHOLD:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient below threshold or LID exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")