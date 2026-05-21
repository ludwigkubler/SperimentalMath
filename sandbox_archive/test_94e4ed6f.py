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
    
    def geometric_entropy(n):
        return n * (math.log(n, 2) + 1)
    
    def communication_complexity(n):
        return n ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        entropy = geometric_entropy(n)
        complexity = communication_complexity(n)
        
        if entropy < complexity:
            return {
                "metric_name": "Communication Complexity",
                "metric_value": complexity,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}: Entropy {entropy} < Complexity {complexity}"
            }
        
        results.append({
            "n": n,
            "entropy": entropy,
            "complexity": complexity
        })
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["entropy"] - mean_entropy) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_entropy,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}: Entropy {results[0]['entropy']} < Complexity {results[0]['complexity']}\" first_failing_seed={first_failing_seed}")