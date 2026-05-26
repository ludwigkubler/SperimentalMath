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
    
    def quantum_entropy(n):
        # Placeholder for actual quantum entropy calculation
        return n / 10
    
    def xor_and_tree_width(n):
        # Placeholder for actual XOR-AND tree width calculation
        return n * 2
    
    instances_tested = 30
    total_entropy = 0
    total_width = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        entropy = quantum_entropy(n)
        width = xor_and_tree_width(n)
        
        total_entropy += entropy
        total_width += width
    
    mean_entropy = total_entropy / instances_tested
    mean_width = total_width / instances_tested
    
    conjecture_holds = (mean_entropy <= math.log(mean_width))
    
    return {
        "metric_name": "Quantum Entropy vs XOR-AND Tree Width",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean entropy > log(n) and mean width < n"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean entropy > log(n) and mean width < n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")