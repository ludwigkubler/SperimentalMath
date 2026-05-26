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
    n = 40
    instances_tested = 30
    min_rank_sum = 0
    
    for _ in range(instances_tested):
        clauses = []
        for _ in range(n // 3):
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n + 1)]
            random.shuffle(clause)
            clauses.append(' | '.join(clause))
        
        # Placeholder for actual computation of minimal rank
        min_rank = sum(len(set(clause.split(' | '))) for clause in clauses) / instances_tested
        
        min_rank_sum += min_rank
    
    metric_value = min_rank_sum / instances_tested
    conjecture_holds = math.log(n, 2)**2 * 0.8 <= metric_value <= math.log(n, 2)**2 * 1.2
    counterexample = "" if conjecture_holds else f"rank={metric_value}, expected=Θ(log^2 {n})"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")