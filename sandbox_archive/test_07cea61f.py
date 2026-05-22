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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_product_disjointness(a, b):
        return all(x != y for x, y in zip(a, b))
    
    def noncrossing_partition_rank(instance):
        n = int(math.log2(len(instance)))
        if 2**n != len(instance):
            return float('inf')
        
        rank = 0
        for i in range(n):
            partition = [set() for _ in range(i+1)]
            for j in range(2**i, 2**(i+1)):
                if instance[j] == 1:
                    partition[random.randint(0, i)].add(j)
            rank += max(len(p) for p in partition)
        return rank
    
    def communication_complexity(instance):
        n = int(math.log2(len(instance)))
        if 2**n != len(instance):
            return float('inf')
        
        # Simplified protocol: each party sends their half
        return n
    
    instances_tested = 0
    total_rank = 0
    total_communication = 0
    
    for _ in range(30):
        instance = generate_instance(random.randint(5, 40))
        rank = noncrossing_partition_rank(instance)
        communication = communication_complexity(instance)
        
        if rank == float('inf') or communication == float('inf'):
            continue
        
        instances_tested += 1
        total_rank += rank
        total_communication += communication
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_rank = total_rank / instances_tested
    mean_communication = total_communication / instances_tested
    
    correlation_coefficient = (mean_rank * mean_communication - 
                               instances_tested * mean_rank * mean_communication) / (
                                   instances_tested * (mean_rank**2 + mean_communication**2) - 
                                   (instances_tested**2 * mean_rank**2 + instances_tested**2 * mean_communication**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_rank <= 1.5 * random.randint(5, 40),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")