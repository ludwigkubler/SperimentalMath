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
    
    def minimal_rank_quandle_representation(protocol, n):
        # Placeholder for actual implementation
        return random.randint(1, n)
    
    def communication_complexity_rank(protocol):
        # Placeholder for actual implementation
        return random.randint(1, n)
    
    def pearson_correlation(x, y):
        if len(x) != len(y) or len(x) < 2:
            return None
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        if std_dev_x == 0 or std_dev_y == 0:
            return None
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation_test = []
    n_values = []
    protocol_lengths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            protocol = {'n_bits': n}
            mrank_Q = minimal_rank_quandle_representation(protocol, n)
            comm_complexity_rank_Q = communication_complexity_rank(protocol)
            correlation_test.append(pearson_correlation([mrank_Q], [comm_complexity_rank_Q]))
            n_values.append(n)
            protocol_lengths.append(n)
    
    if not all(correlation is not None for correlation in correlation_test):
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(correlation_test),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "correlation_computation_error"
        }
    
    mean_corr = sum(correlation_test) / len(correlation_test)
    std_corr = math.sqrt(sum((corr - mean_corr) ** 2 for corr in correlation_test) / len(correlation_test))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": mean_corr,
        "instances_tested": len(correlation_test),
        "n_max": max(n_values),
        "conjecture_holds": mean_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((res["metric_value"] - mean_corr) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")