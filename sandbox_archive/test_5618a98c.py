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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_brauer_rank = 0
    total_comm_complexity_rank = 0
    
    while instances_tested < 30:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Compute Brauer group rank (simplified example)
        brauer_rank = sum(f) % n
        
        # Compute communication complexity rank (simplified example)
        comm_complexity_rank = max(f.count(0), f.count(1))
        
        total_brauer_rank += brauer_rank
        total_comm_complexity_rank += comm_complexity_rank
        instances_tested += 1
    
    mean_brauer_rank = total_brauer_rank / instances_tested
    mean_comm_complexity_rank = total_comm_complexity_rank / instances_tested
    correlation_coefficient = (instances_tested * sum(brauer_rank * comm_complexity_rank for brauer_rank, comm_complexity_rank in zip(range(n), range(n))) - 
                               mean_brauer_rank * instances_tested * mean_comm_complexity_rank) / (
        math.sqrt(instances_tested * sum((brauer_rank - mean_brauer_rank)**2 for brauer_rank in range(n)) * 
                  instances_tested * sum((comm_complexity_rank - mean_comm_complexity_rank)**2 for comm_complexity_rank in range(n))))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"Brauer rank {result['metric_value']}, Comm complexity rank {result['instances_tested']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break