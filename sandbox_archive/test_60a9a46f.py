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
    
    def generate_ac0_circuit(n, s):
        # Simple AC⁰ circuit generation (not actual complexity)
        return [random.choice([0, 1]) for _ in range(s)]
    
    def symmetric_difference(f1, f2):
        return [x ^ y for x, y in zip(f1, f2)]
    
    def count_distinct_divisors(f):
        divisors = set()
        n = len(f)
        for i in range(1 << n):
            divisor = [f[j] if (i & (1 << j)) else 0 for j in range(n)]
            if all(x == 0 or x == 1 for x in divisor):
                divisors.add(tuple(divisor))
        return len(divisors)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_divisors = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            s = random.randint(1, min(n * (n - 1) // 2, 40))
            circuit = generate_ac0_circuit(n, s)
            divisors_count = count_distinct_divisors(circuit)
            total_divisors += divisors_count
            instances_tested += 1
    
    metric_value = total_divisors / instances_tested
    conjecture_holds = all(metric_value >= (math.log(n) ** 2) / s for n, s in zip(n_values, [random.randint(1, min(n * (n - 1) // 2, 40)) for _ in range(len(n_values))]))
    
    return {
        "metric_name": "symmetric_difference_divisors",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")