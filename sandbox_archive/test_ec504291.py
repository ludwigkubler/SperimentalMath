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
    
    def generate_circuit(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_circuit(n // 2, d - 1)
            outputs = []
            for i in range(len(inputs)):
                for j in range(len(inputs)):
                    outputs.append((inputs[i] & inputs[j]) | (inputs[i] ^ inputs[j]))
            return outputs
    
    def hausdorff_dimension(points):
        if len(points) < 2:
            return 0
        min_distance = float('inf')
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
                min_distance = min(min_distance, distance)
        return math.log(len(points)) / math.log(1 / min_distance)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, random.randint(1, 10))
            true_points = [(i, 1) for i, x in enumerate(circuit) if x == 1]
            dim = hausdorff_dimension(true_points)
            results.append((n, dim))
    
    n_max = max(max(x[0] for x in results), min(n_values))
    instances_tested = len(results)
    
    correlation_sum = 0
    n_sum = 0
    
    for n, dim in results:
        correlation_sum += (dim - math.log(n) / math.log(2)) ** 2
        n_sum += n
    
    mean_dim = sum(dim for _, dim in results) / instances_tested
    variance = correlation_sum / instances_tested
    std_dev = math.sqrt(variance)
    
    correlation_coefficient = (sum((n - n_sum / instances_tested) * (dim - mean_dim) for n, dim in results) /
                                (instances_tested * std_dev * math.sqrt(n_sum / instances_tested)))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation < 0.8"
    
    return {
        "metric_name": "Hausdorff dimension",
        "metric_value": mean_dim,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(i for i, x in enumerate(results) if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data n_tested=30")