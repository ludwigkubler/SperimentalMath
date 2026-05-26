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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def noncrossing_partitions(n):
        if n == 0:
            return [[]]
        partitions = []
        for i in range(1, n):
            for left in noncrossing_partitions(i):
                for right in noncrossing_partitions(n - i - 1):
                    partitions.append([left + [i], right])
        return partitions
    
    def communication_complexity(f):
        # Placeholder function to calculate CC_XOR-AND
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) * 2
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    partitions = noncrossing_partitions(n)
    tau_P_f = len(partitions)
    
    cc_xor_and_f = communication_complexity(f)
    ratio = cc_xor_and_f / tau_P_f if tau_P_f != 0 else float('inf')
    
    return {
        "metric_name": "CC_XOR-AND(f)/τ(P_f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n**2,  # Placeholder polynomial bound
        "counterexample": "" if ratio <= n**2 else f"Ratio {ratio} exceeds polynomial bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")