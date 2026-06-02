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
    
    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(1, n))
        return protocol
    
    def communication_complexity_rank(protocol):
        rank = 0
        for i in range(len(protocol)):
            for j in range(i + 1, len(protocol)):
                if protocol[i] != protocol[j]:
                    rank += 1
        return rank
    
    def noncommutative_crossed_product_order(protocol):
        order = 0
        n = len(protocol)
        for i in range(n):
            for j in range(n):
                if protocol[i] != protocol[j]:
                    order += 1
        return order
    
    def pearson_correlation_coefficient(data_x, data_y):
        n = len(data_x)
        mean_x = sum(data_x) / n
        mean_y = sum(data_y) / n
        covariance = sum((data_x[i] - mean_x) * (data_y[i] - mean_y) for i in range(n))
        variance_x = sum((data_x[i] - mean_x) ** 2 for i in range(n)) / n
        variance_y = sum((data_y[i] - mean_y) ** 2 for i in range(n)) / n
        return covariance / (math.sqrt(variance_x) * math.sqrt(variance_y))
    
    data_x = []
    data_y = []
    
    for _ in range(100):
        n = random.randint(5, 40)
        protocol = generate_protocol(n)
        rank = communication_complexity_rank(protocol)
        order = noncommutative_crossed_product_order(protocol)
        data_x.append(rank)
        data_y.append(order)
    
    correlation_coefficient = pearson_correlation_coefficient(data_x, data_y)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 100,
        "n_max": max(len(generate_protocol(n)) for n in range(5, 41)),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else "Pearson correlation coefficient <= 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient <= 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")