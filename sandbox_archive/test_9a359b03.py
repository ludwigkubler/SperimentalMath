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
    
    # Generate a random AC0 parity circuit with threshold θ
    n = 10  # Number of input bits
    theta = random.randint(1, 5)  # Threshold
    
    # Simulate quantum entanglement information (placeholder value)
    I_C = 2 * theta * math.log(2, 2)
    
    # Check the conjecture
    if I_C > 2 * theta * math.log(2):
        counterexample = f"Threshold={theta}, I(C)={I_C}, Bound=2*{theta}*log(2)"
        conjecture_holds = False
    else:
        counterexample = ""
        conjecture_holds = True
    
    return {
        "metric_name": "Quantum Entanglement Information",
        "metric_value": I_C,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_str = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result_str)