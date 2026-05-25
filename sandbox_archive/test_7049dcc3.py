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
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in set(f)]
        probs = [c / n for c in counts]
        return -sum(p * math.log2(p) if p > 0 else 0 for p in probs)

    def geometric_langlands_rank(f):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(f))

    instances_tested = 100
    rank_sum = 0
    entropy_sum = 0
    rank_squared_sum = 0
    entropy_product_sum = 0

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(n)]
        rank = geometric_langlands_rank(f)
        entropy = shannon_entropy(f)
        
        rank_sum += rank
        entropy_sum += entropy
        rank_squared_sum += rank ** 2
        entropy_product_sum += rank * entropy

    mean_rank = rank_sum / instances_tested
    mean_entropy = entropy_sum / instances_tested
    variance_rank = (rank_squared_sum / instances_tested) - (mean_rank ** 2)
    covariance = (entropy_product_sum / instances_tested) - (mean_rank * mean_entropy)

    if variance_rank == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    pearson_corr = covariance / math.sqrt(variance_rank * (entropy_sum ** 2 / instances_tested))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "conjecture_holds": pearson_corr >= 0.7 and sum(1 for _ in range(instances_tested) if geometric_langlands_rank([random.choice([0, 1]) for _ in range(n)]) > shannon_entropy([random.choice([0, 1]) for _ in range(n)])) / instances_tested <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")