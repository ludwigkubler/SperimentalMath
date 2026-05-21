# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product

def evaluate_instance(instance, assignment):
    return sum(assignment[i] ^ instance[i][j] for i in range(len(instance)) for j in range(len(instance[i]))) % 2 == 0

def compute_LW(instance, alpha):
    n = len(instance)
    tau = 1 - 1 / (8 * alpha)
    S_tau = {tuple(sorted([assignment[i] if i != j else 1 - assignment[j] for j in range(n)])) 
              for assignment in product([0, 1], repeat=n) 
              if evaluate_instance(instance, assignment) >= tau * len(instance)}
    
    total_size = len(S_tau)
    marginal_sizes = [len({tuple(sorted([x[i] if i != j else 1 - x[j] for j in range(n)])) for x in S_tau}) for i in range(n)]
    
    LW = sum(math.log2(size) for size in marginal_sizes) / n - math.log2(total_size)
    return LW

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [14, 16, 18, 20]
    alpha_values = [0.5, 0.7, 0.85, 0.918, 1.00, 1.10, 1.50]
    
    results = []
    for n in n_values:
        for alpha in alpha_values:
            instance = [[random.randint(0, 1) for _ in range(n)] for _ in range(alpha * n)]
            LW = compute_LW(instance, alpha)
            results.append(LW / n)
    
    mean_LW = sum(results) / len(results)
    std_LW = (sum((x - mean_LW) ** 2 for x in results) / len(results)) ** 0.5
    
    conjecture_holds = all(0 <= LW < 0.02 for LW in results if alpha <= 0.85) and \
                        all(LW > 0.05 for LW in results if alpha >= 1.10)
    
    return {
        "metric_name": "LW/alpha",
        "metric_value": mean_LW,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_LW = sum(results) / len(results)
    std_LW = (sum((x - mean_LW) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if 0 <= r < 0.02 and 0.85 <= alpha_values[results.index(r)]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_LW} std={std_LW} support_fraction={support_fraction}")
    elif any(0.85 <= r < 0.02 for r in results):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(r for r in results if 0.85 <= r < 0.02))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")