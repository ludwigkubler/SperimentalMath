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
    
    def morse_function(f):
        n = len(f)
        count_0 = 0
        for i in range(n):
            if f[i] == 0:
                count_0 += 1
        return count_0
    
    def communication_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != 0:
                rank += 1
        return rank
    
    def topological_entropy(h):
        return h / math.log2(len(h))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(n)]
        morse_f = morse_function(f)
        r_f = communication_rank(f)
        h_morse_f = topological_entropy(morse_f)
        
        results.append({
            "n": n,
            "f": f,
            "morse_f": morse_f,
            "r_f": r_f,
            "h_morse_f": h_morse_f
        })
    
    correlation_sum = 0
    for result in results:
        correlation_sum += (result["h_morse_f"] - result["r_f"]) / math.sqrt(len(result["f"]))
    
    mean_correlation = correlation_sum / len(results)
    std_deviation = 0
    for result in results:
        std_deviation += ((result["h_morse_f"] - result["r_f"] - mean_correlation) ** 2) / (len(results) - 1)
    std_deviation = math.sqrt(std_deviation)
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(mean_correlation) <= 2 ** n / 3,
        "counterexample": "" if abs(mean_correlation) <= 2 ** n / 3 else "mean_correlation_outside_bound"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_correlation_outside_bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")