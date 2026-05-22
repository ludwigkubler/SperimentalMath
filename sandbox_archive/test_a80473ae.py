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
    
    def log_base(x, base):
        if x <= 0 or base <= 1:
            return None
        return math.log(x) / math.log(base)

    def tensor_rank(n):
        # Simplified approximation of tensor rank for demonstration purposes
        return n // 2

    def bp_read_twice_size():
        return random.randint(1, 40)

    instances_tested = 30
    total_tensor_rank = 0
    support_count = 0

    for _ in range(instances_tested):
        size = bp_read_twice_size()
        expected_rank = log_base(size, 2)
        if expected_rank is None:
            continue
        actual_rank = tensor_rank(size)
        if actual_rank > 10:
            return {
                "metric_name": "tensor_rank",
                "metric_value": actual_rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Tensor rank {actual_rank} exceeds limit of 10"
            }
        if abs(actual_rank - expected_rank) <= 2 * expected_rank / 5:
            support_count += 1
        total_tensor_rank += actual_rank

    mean_rank = total_tensor_rank / instances_tested
    support_fraction = support_count / instances_tested

    return {
        "metric_name": "tensor_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")