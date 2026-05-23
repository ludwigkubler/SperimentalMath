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
        bp = [random.randint(0, 1) for _ in range(n)]
        return bp
    
    def read_twice_complexity(bp):
        n = len(bp)
        complexity = 0
        for i in range(n):
            if bp[i] == 1:
                complexity += sum(bp[j] for j in range(i + 1, n))
        return complexity
    
    def tensor_network_size(bp):
        n = len(bp)
        size = 2 ** n
        return size
    
    def entanglement_entropy(size):
        if size <= 0:
            return None
        entropy = -size * math.log2(1 / size) / math.log2(size)
        return entropy
    
    def bp_read_twice_width(bp):
        n = len(bp)
        width = 0
        for i in range(n):
            if bp[i] == 1:
                width += sum(bp[j] for j in range(i + 1, n))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different BPs
            bp = generate_bp(n)
            complexity = read_twice_complexity(bp)
            size = tensor_network_size(bp)
            entropy = entanglement_entropy(size)
            width = bp_read_twice_width(bp)
            
            if entropy is not None:
                total_entropy += entropy
                instances_tested += 1
            
            if entropy is not None and entropy >= n:
                conjecture_holds = False
                counterexample = f"BP of size {n} with read-twice complexity {complexity}, entanglement entropy {entropy}"
                break
    
    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else None
    support_fraction = instances_tested / (len(n_values) * 5)
    
    return {
        "metric_name": "Entanglement Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_entropy = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else None
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["instances_tested"] > 0 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support found")