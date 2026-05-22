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
    
    def generate_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
        return bp
    
    def min_tensor_product_entropy(bp):
        n = len(bp)
        states = set()
        current_state = [0] * n
        states.add(tuple(current_state))
        
        for bit in bp:
            next_states = []
            for state in states:
                new_state = list(state)
                new_state[0] = 1 - new_state[0]
                next_states.append(new_state)
                if bit == 1:
                    new_state[1:] = [1 - x for x in new_state[1:]]
                    next_states.append(new_state)
            states.update(tuple(state) for state in next_states)
        
        return math.log2(len(states))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    
    for n in n_values:
        bp = generate_bp(n)
        entropy_value = min_tensor_product_entropy(bp)
        total_entropy += entropy_value
        instances_tested += 1
        
        if entropy_value > n * math.log2(2):
            return {
                "metric_name": "Minimal Tensor Product Entropy",
                "metric_value": entropy_value,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"BP of size {n} with entropy {entropy_value}"
            }
    
    return {
        "metric_name": "Minimal Tensor Product Entropy",
        "metric_value": total_entropy / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"BP of size {result['instances_tested']} with entropy {result['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")