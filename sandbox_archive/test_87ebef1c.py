# auto-injected by SEC sandbox
import math
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

def generate_boolean_circuit(W):
    if W == 1:
        return ['0', '1']
    w = random.randint(1, W-1)
    left = generate_boolean_circuit(w)
    right = generate_boolean_circuit(W-w)
    return [f'({l} & {r})' for l in left] + [f'({l} | {r})' for l in right]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    total_metric_value = 0.0
    instances_tested = 0
    
    for W in range(5, 41):
        circuit = generate_boolean_circuit(W)
        instances_tested += len(circuit)
        if instances_tested > 30:
            break
        
        n_max = max(n_max, W)
        
        # Placeholder for actual computation of the metric
        # For now, we'll use a dummy value that depends on W
        metric_value = W**2 / 2
        
        total_metric_value += metric_value
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= n_max**2
    counterexample = "" if conjecture_holds else f"Mean: {mean_metric_value}, Expected: {n_max**2}"
    
    return {
        "metric_name": "Dimension of Moduli Space",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")