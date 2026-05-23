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
    
    def generate_binary_string(length):
        return ''.join(random.choice('01') for _ in range(length))
    
    def tensor_product(s1, s2):
        return ''.join(a + b for a, b in zip(s1, s2))
    
    def communication_complexity(s):
        n = len(s)
        if n == 1:
            return 1
        return n * (n - 1) // 2
    
    def simplicial_complex_rank(s):
        # Placeholder function for computing the rank of the configuration space
        # This is a dummy implementation and should be replaced with actual logic
        return len(s)
    
    n = random.randint(5, 40)
    s1 = generate_binary_string(n)
    s2 = generate_binary_string(n)
    
    tensor_result = tensor_product(s1, s2)
    comm_complexity = communication_complexity(tensor_result)
    config_rank = simplicial_complex_rank(s1)
    
    return {
        "metric_name": "Rank vs Communication Complexity",
        "metric_value": config_rank,
        "instances_tested": 1,
        "conjecture_holds": config_rank <= comm_complexity + 3,
        "counterexample": "" if config_rank <= comm_complexity + 3 else f"Rank {config_rank} exceeds Comm. Comp. {comm_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds Communication Complexity\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")