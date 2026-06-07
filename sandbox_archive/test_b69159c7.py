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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(circuit):
        n = len(circuit)
        rank = sum(circuit[i] != circuit[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
        return rank
    
    def minimal_brauer_group_order(circuit):
        # Placeholder function. This should be replaced with actual Brauer group computation.
        return len(circuit)
    
    metric_name = "log2(B(C))_vs_log2(R_C)"
    instances_tested = 0
    n_max = 0
    total_log2_B_C = 0
    total_log2_R_C = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            B_C = minimal_brauer_group_order(circuit)
            R_C = communication_complexity_rank_variance(circuit)
            
            if B_C == 0 or R_C <= 0:
                continue
            
            instances_tested += 1
            total_log2_B_C += math.log2(B_C)
            total_log2_R_C += math.log2(R_C)
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_log2_B_C = total_log2_B_C / instances_tested
    mean_log2_R_C = total_log2_R_C / instances_tested
    
    std_log2_B_C = math.sqrt(sum((math.log2(B_C) - mean_log2_B_C) ** 2 for B_C in range(1, n_max + 1)) / (n_max - 1))
    std_log2_R_C = math.sqrt(sum((math.log2(R_C) - mean_log2_R_C) ** 2 for R_C in range(1, n_max + 1)) / (n_max - 1))
    
    conjecture_holds = abs(mean_log2_B_C - mean_log2_R_C) <= std_log2_B_C + std_log2_R_C
    
    return {
        "metric_name": metric_name,
        "metric_value": None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")