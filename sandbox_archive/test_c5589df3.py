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
        protocol = []
        for _ in range(n):
            input_size = random.randint(1, n)
            output_size = random.randint(1, n)
            protocol.append((input_size, output_size))
        return protocol
    
    def calculate_crossed_product_order(protocol):
        # Simplified mapping to a non-commutative algebra structure
        order = 0
        for input_size, output_size in protocol:
            order += input_size * output_size
        return order
    
    def calculate_rank_variance(protocol):
        # Simplified calculation of rank variance
        n = len(protocol)
        total_input_size = sum(input_size for input_size, _ in protocol)
        total_output_size = sum(output_size for _, output_size in protocol)
        mean_input = total_input_size / n
        mean_output = total_output_size / n
        variance_input = sum((input_size - mean_input) ** 2 for input_size, _ in protocol) / n
        variance_output = sum((output_size - mean_output) ** 2 for _, output_size in protocol) / n
        rank_variance = (variance_input + variance_output) / 2
        return rank_variance
    
    def linear_regression(x, y):
        n = len(x)
        if n < 2:
            return None, None
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    def correlation_coefficient(x, y):
        n = len(x)
        if n < 2:
            return None
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    log_min_orders = []
    rank_variances = []
    
    for n in n_values:
        protocol = generate_protocol(n)
        min_order = calculate_crossed_product_order(protocol)
        rank_variance = calculate_rank_variance(protocol)
        
        if min_order <= 0 or rank_variance <= 0:
            continue
        
        log_min_orders.append(math.log(min_order))
        rank_variances.append(rank_variance)
    
    if not log_min_orders or not rank_variances:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(log_min_orders),
            "n_max": max(n_values) if n_values else 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    slope, _ = linear_regression(log_min_orders, rank_variances)
    correlation = correlation_coefficient(log_min_orders, rank_variances)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(log_min_orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_data")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")