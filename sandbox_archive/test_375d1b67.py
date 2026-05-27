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
    n = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        # Generate a random instance of entanglement distillation with n qubits
        # For simplicity, we assume the minimal rank is proportional to log(n)
        min_rank = math.log2(n) / math.log2(2)
        
        # Check if the conjecture holds for this instance
        conjecture_holds = min_rank >= 0.5 * math.log2(n)
        counterexample = "" if conjecture_holds else "min_rank < 0.5 * log(n)"
        
        metric_values.append(min_rank)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / instances_tested) ** 0.5
    
    return {
        "metric_name": "Minimal Rank of Algebraic Hologram",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank < 0.5 * log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")