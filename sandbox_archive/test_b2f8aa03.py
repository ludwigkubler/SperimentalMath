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
    
    # Define constants and parameters
    c = 1.0  # Constant for the conjecture bound
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    # Initialize variables to track results
    total_metric_value = 0
    num_supporting_seeds = 0
    counterexample_found = False
    first_failing_seed = None
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        
        # Simulate communication complexity rank r (for simplicity, use a random integer)
        r = random.randint(1, 5)  # Limiting the rank to a small range for practical testing
        
        # Calculate the minimal dimension of the Hodge structure based on the conjecture
        hodge_dimension = c * r ** 2
        
        # Simulate the communication complexity instance (for simplicity, use a random integer)
        comm_complexity_rank = random.randint(1, 5)  # Limiting the rank to a small range for practical testing
        
        # Check if the conjecture holds
        if hodge_dimension >= comm_complexity_rank:
            total_metric_value += hodge_dimension
            num_supporting_seeds += 1
        else:
            counterexample_found = True
            first_failing_seed = seed
    
    # Calculate mean and standard deviation of the metric values
    mean_metric_value = total_metric_value / instances_per_seed
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in range(instances_per_seed)) / instances_per_seed) ** 0.5
    
    # Determine if the conjecture holds based on the seeds tested
    if counterexample_found:
        result = "FALSIFIED"
        counterexample = f"Seed {first_failing_seed} failed with hodge_dimension < comm_complexity_rank"
    elif num_supporting_seeds / instances_per_seed >= 0.8:
        result = "SUPPORTED"
        support_fraction = num_supporting_seeds / instances_per_seed
    else:
        result = "INCONCLUSIVE"
        support_fraction = None
    
    return {
        "metric_name": "Hodge Dimension",
        "metric_value": mean_metric_value,
        "instances_tested": instances_per_seed,
        "n_max": n_max,
        "conjecture_holds": result == "SUPPORTED",
        "counterexample": counterexample if counterexample else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default list of prime seeds
    
    results = []
    for seed in seeds:
        result_dict = run_trial(seed)
        print(f"TRIAL: {result_dict}")
        results.append(result_dict)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_metric_value = (sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {result} mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")