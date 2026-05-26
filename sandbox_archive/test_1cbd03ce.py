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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def hodge_rank(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a valid n-bit boolean function")
    
    count_0 = [0] * n
    count_1 = [0] * n
    
    for x in f:
        for i in range(n):
            if x & (1 << i) == 0:
                count_0[i] += 1
            else:
                count_1[i] += 1
    
    rank = max(max(count_0), max(count_1))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            rank = hodge_rank(f)
            total_rank += rank
            instances_tested += 1
        
        avg_rank = Fraction(total_rank, instances_tested)
        results.append(avg_rank)
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    
    conjecture_holds = all(rank <= 2 * n_values[i] for i, rank in enumerate(results))
    counterexample = "" if conjecture_holds else f"rank={results[0]}, expected=2*{n_values[0]}"
    
    return {
        "metric_name": "avg_hodge_rank",
        "metric_value": float(mean_value),
        "instances_tested": len(n_values) * 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2 * max(n_values)) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r > 2 * max(n_values) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r > 2 * max(n_values)))]
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")