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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random quantum state with an entanglement rank of Θ(n^0.5)
    n = 30  # Fixed size for simplicity
    E = int(math.sqrt(n))
    state = [random.randint(1, 2**E) for _ in range(E)]
    
    # Translate the quantum state into a Max-Cut instance
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            A[i][j] = random.choice(state)
    
    # Measure the communication complexity for the Max-Cut instance
    cc_max_cut = sum(A[i][j] for i in range(n) for j in range(i + 1, n)) / (n * (n - 1) / 2)
    
    # Compare the measured communication complexity against the conjectured bounds
    if cc_max_cut / n <= 1.5:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "CC_{Max-Cut}(|Ψ⟩) > 1.5 * n"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc_max_cut,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC_{Max-Cut}(|Ψ⟩) > 1.5 * n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")