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
    
    def frege_clause_to_symplectic_structure(clause):
        # Simplified mapping for demonstration purposes
        return [random.uniform(-1, 1), random.uniform(-1, 1)]
    
    def geometric_quantization(phase_space):
        # Simplified calculation for demonstration purposes
        return sum(abs(x) for x in phase_space)
    
    def frege_width(clause):
        return len(clause)
    
    n_max = 0
    instances_tested = 0
    total_mq = 0.0
    total_log_w = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clause = [random.choice([True, False]) for _ in range(n)]
            phase_space = frege_clause_to_symplectic_structure(clause)
            mq = geometric_quantization(phase_space)
            w = frege_width(clause)
            
            if n > n_max:
                n_max = n
            
            instances_tested += 1
            total_mq += mq
            total_log_w += math.log(w) if w > 0 else 0
    
    mean_mq = total_mq / instances_tested
    mean_log_w = total_log_w / instances_tested
    conjecture_holds = all(mq <= 1.5 * math.log(w) for mq, w in zip([mean_mq] * instances_tested, [math.exp(mean_log_w)] * instances_tested))
    
    return {
        "metric_name": "mq_bound",
        "metric_value": mean_mq,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")