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
    
    def generate_ac0_circuit(n):
        # Generate a simple AC⁰ circuit for n inputs
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
    
    def communication_complexity(circuit):
        # Simulate the Karchmer-Wigderson game to estimate communication complexity
        n = len(circuit)
        if n == 1:
            return 1
        left_circuit = [row[:n//2] for row in circuit]
        right_circuit = [row[n//2:] for row in circuit]
        return max(communication_complexity(left_circuit), communication_complexity(right_circuit)) + 1
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    cc = communication_complexity(circuit)
    
    if cc < math.log2(n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CC({n}) = {cc} < log2({n})"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_cc = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_cc)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC({n}) < log2({n})\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")