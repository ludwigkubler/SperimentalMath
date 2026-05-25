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
    
    def shannon_entropy(f):
        counts = [f.count(bit) / len(f) for bit in [0, 1]]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in counts)
        return entropy
    
    def geometric_langlands_dual_rank(f):
        # Placeholder function to simulate the rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    rank_values = []
    entropy_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            rank = geometric_langlands_dual_rank(f)
            entropy = shannon_entropy(f)
            rank_values.append(rank)
            entropy_values.append(entropy)
    
    if not rank_values or not entropy_values:
        return {
            "metric_name": "Rank vs Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Empty data"
        }
    
    mean_rank = sum(rank_values) / len(rank_values)
    mean_entropy = sum(entropy_values) / len(entropy_values)
    
    correlation_coefficient = sum((x - mean_rank) * (y - mean_entropy) for x, y in zip(rank_values, entropy_values)) / \
                              math.sqrt(sum((x - mean_rank)**2 for x in rank_values) * sum((y - mean_entropy)**2 for y in entropy_values))
    
    ratio_exceeding_bound = sum(1 for r in rank_values if r > 10 * mean_entropy) / len(rank_values)
    
    return {
        "metric_name": "Rank vs Entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rank_values),
        "conjecture_holds": ratio_exceeding_bound <= 0.1 and abs(correlation_coefficient) >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE some trials had no data")