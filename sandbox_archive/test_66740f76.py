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
    
    def generate_protocol(n):
        # Generate a simple n-communication protocol as an example
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_lid(protocol):
        # Placeholder for LID calculation
        return len(set(protocol))
    
    def calculate_comm_rank_var(protocol):
        # Placeholder for communication complexity rank variance calculation
        return sum([x**2 for x in protocol]) / len(protocol)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_protocol(n)
        lid = calculate_lid(protocol)
        comm_rank_var = calculate_comm_rank_var(protocol)
        
        if lid > 3 * comm_rank_var + 1:  # Example condition to check
            return {
                "metric_name": "LID vs CommRankVar",
                "metric_value": lid,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "LID > 3 * CommRankVar + 1"
            }
        
        results.append({
            "n": n,
            "lid": lid,
            "comm_rank_var": comm_rank_var
        })
    
    if len(results) < 30:
        return {
            "metric_name": "LID vs CommRankVar",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    lid_values = [r["lid"] for r in results]
    comm_rank_var_values = [r["comm_rank_var"] for r in results]
    
    mean_lid = sum(lid_values) / len(lid_values)
    mean_comm_rank_var = sum(comm_rank_var_values) / len(comm_rank_var_values)
    variance_lid = sum((x - mean_lid)**2 for x in lid_values) / len(lid_values)
    variance_comm_rank_var = sum((x - mean_comm_rank_var)**2 for x in comm_rank_var_values) / len(comm_rank_var_values)
    
    correlation_coefficient = (sum((lid_values[i] - mean_lid) * (comm_rank_var_values[i] - mean_comm_rank_var) for i in range(len(lid_values))) /
                               math.sqrt(variance_lid * variance_comm_rank_var))
    
    return {
        "metric_name": "LID vs CommRankVar",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(lid <= 3 * mean_comm_rank_var + 1 for lid in lid_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["instances_tested"] >= 30 for r in results):
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        n_tested = sum(r["instances_tested"] for r in results)
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={n_tested}")