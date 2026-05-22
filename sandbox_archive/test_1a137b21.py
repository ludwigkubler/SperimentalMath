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
    
    def compute_characteristic_function(f):
        n = int(math.log2(len(f)))
        char_func = [0] * (2**n)
        for i in range(len(f)):
            char_func[i] = f[i]
        return char_func
    
    def compute_influence_complexity(char_func):
        n = int(math.log2(len(char_func)))
        influence = 0
        for i in range(n):
            bit_flips = [char_func[j ^ (1 << i)] for j in range(2**n)]
            influence += sum(bit_flips) / len(bit_flips)
        return influence
    
    def compute_norm(char_func):
        norm = 0
        for val in char_func:
            norm += val ** 2
        return math.sqrt(norm)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_influence_complexity = 0
    total_norm_squared = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            char_func = compute_characteristic_function(f)
            influence_complexity = compute_influence_complexity(char_func)
            norm = compute_norm(char_func)
            
            total_influence_complexity += influence_complexity
            total_norm_squared += norm ** 2
            instances_tested += 1
    
    mean_influence_complexity = total_influence_complexity / instances_tested
    mean_norm_squared = total_norm_squared / instances_tested
    
    correlation_coefficient = (instances_tested * mean_influence_complexity * mean_norm_squared -
                               sum(influence_complexity * norm_squared for influence_complexity, norm_squared in zip(
                                   [mean_influence_complexity] * instances_tested,
                                   [mean_norm_squared] * instances_tested))) / (
        math.sqrt((instances_tested * mean_influence_complexity ** 2 - sum(influence_complexity ** 2
                                                                            for influence_complexity in
                                                                            [mean_influence_complexity] *
                                                                            instances_tested)) *
                  (instances_tested * mean_norm_squared ** 2 - sum(norm_squared ** 2
                                                                    for norm_squared in
                                                                    [mean_norm_squared] * instances_tested))))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")