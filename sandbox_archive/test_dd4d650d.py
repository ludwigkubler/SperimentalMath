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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_comm_cost = 0
        for i in range(2**n):
            comm_cost = sum(abs(f[i] - f[j]) for j in range(i+1, 2**n)) / (2**(n-1))
            if comm_cost > max_comm_cost:
                max_comm_cost = comm_cost
        return max_comm_cost
    
    def frobenius_norm(V):
        n = len(V)
        sum_of_squares = sum(sum(x**2 for x in row) for row in V)
        return math.sqrt(n * sum_of_squares)
    
    def generate_variety(f):
        n = len(f)
        variety = []
        for i in range(2**n):
            if all(f[i] == f[j] for j in range(i+1, 2**(n-1))):
                variety.append([f[i]] * (2**(n-1)))
        return variety
    
    def pearson_correlation(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        numerator = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n))
        denominator = math.sqrt(sum((X[i] - mean_X)**2 for i in range(n))) * math.sqrt(sum((Y[i] - mean_Y)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        comm_rank = communication_complexity(f)
        V = generate_variety(f)
        frobenius_norm_value = frobenius_norm(V)
        results.append((comm_rank, frobenius_norm_value))
    
    X, Y = zip(*results)
    correlation_coefficient = pearson_correlation(X, Y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")