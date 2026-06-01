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
    # Set seed for reproducibility
    random.seed(seed)
    
    # Define a simple function to generate modular forms and circuits
    def generate_modular_form(level, weight):
        # Placeholder for actual modular form generation logic
        return level * weight
    
    def construct_circuit(modular_form_value):
        # Placeholder for actual circuit construction logic
        return modular_form_value + 1
    
    def compute_minimal_order(modular_form_value):
        # Placeholder for actual minimal order computation logic
        return abs(modular_form_value)
    
    def compute_monotone_width(circuit):
        # Placeholder for actual monotone width computation logic
        return len(circuit)
    
    # Define the range of levels and weights to test
    levels = [5, 10, 15, 20, 30, 40]
    weights = [1, 2, 3, 4, 5]
    
    # Initialize variables for the trial
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    # Run multiple trials with different levels and weights
    for level in levels:
        for weight in weights:
            modular_form_value = generate_modular_form(level, weight)
            circuit = construct_circuit(modular_form_value)
            minimal_order = compute_minimal_order(modular_form_value)
            monotone_width = compute_monotone_width(circuit)
            
            # Record the metric value
            metric_values.append(minimal_order / monotone_width)
            instances_tested += 1
            n_max = max(n_max, level)
    
    # Compute the mean and standard deviation of the metric values
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    # Check if the conjecture holds based on the correlation
    correlations = [(x, y) for x, y in zip(metric_values[:-1], metric_values[1:])]
    correlation_coefficient = sum((x - mean_metric_value) * (y - mean_metric_value) for x, y in correlations) / len(correlations)
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(len(correlations) / 2)))
    
    # Determine if the conjecture holds
    conjecture_holds = abs(correlation_coefficient) >= 0.7 and p_value <= 0.05
    
    # Return the trial results as a dictionary
    return {
        "metric_name": "Correlation between minimal order and monotone width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute the mean and standard deviation of the metric values
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    
    # Compute the fraction of seeds where the conjecture holds
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    # Determine the final result
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")