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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        count = sum(f[i] != f[i + 1] for i in range(len(f) - 1))
        return math.ceil(count / (2 * n))
    
    def noncrossing_partition_rank(n):
        # Placeholder function, as mapping is undefined for n > 4
        if n > 4:
            return "mapping_undefined"
        return random.randint(1, n)
    
    metric_name = "communication_complexity_vs_noncrossing_partition_rank"
    instances_tested = 30
    total_metric_value = 0
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(5, 40))
        C_f = communication_complexity(f)
        tau_noncrossing_partition = noncrossing_partition_rank(len(f))
        
        if tau_noncrossing_partition == "mapping_undefined":
            return {
                "metric_name": metric_name,
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        total_metric_value += abs(C_f - tau_noncrossing_partition)
    
    mean_difference = total_metric_value / instances_tested
    conjecture_holds = mean_difference <= 3
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_difference,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*37, 149))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")