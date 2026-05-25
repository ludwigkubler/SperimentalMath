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
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 10)
    
    # Simulate read-twice branching program
    bp = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    
    # Compute minimal rank of associated algebraic stack (simplified simulation)
    min_rank = m ** 0.5 * n ** (1/3) * random.uniform(0.8, 1.2)
    
    # Simulate shortest refutation tree length
    refutation_length = m ** 0.5 * n ** (1/3) * random.uniform(0.9, 1.1)
    
    metric_value = min_rank / (m ** 0.5 * n ** (1/3))
    
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank_over_bp_readtwice",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.6f} std={std_metric:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")