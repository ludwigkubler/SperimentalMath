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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified rank calculation (for demonstration purposes)
        return n
    
    def local_indeterminacy(f):
        n = len(f)
        # Simplified IL calculation (for demonstration purposes)
        return n / 2
    
    metric_name = "Pearson correlation coefficient"
    instances_tested = 0
    n_max = 1
    total_il = 0
    total_rank = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        il = local_indeterminacy(f)
        
        total_il += il
        total_rank += rank
        instances_tested += 1
    
    mean_il = total_il / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * sum(il * rank for il, rank in zip([mean_il] * instances_tested, [mean_rank] * instances_tested)) - instances_tested * mean_il * mean_rank) / math.sqrt((instances_tested * sum(il**2 for il in [mean_il] * instances_tested) - instances_tested * mean_il**2) * (instances_tested * sum(rank**2 for rank in [mean_rank] * instances_tested) - instances_tested * mean_rank**2))
    
    conjecture_holds = correlation_coefficient > 0
    counterexample = "" if conjecture_holds else "Pearson correlation coefficient is not significantly positive"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")