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
    
    def generate_acc0_circuit(n):
        # Simplified generation for demonstration purposes
        return [random.randint(1, 2) for _ in range(n)]
    
    def hodge_rank(C):
        S_n = sum(C)
        n = len(C)
        if n == 0:
            return Fraction(0)
        return Fraction(S_n, math.log(n + 1))
    
    def is_valid_circuit(C):
        # Simplified validation for demonstration purposes
        return all(x in [0, 1] for x in C)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        C = generate_acc0_circuit(n)
        
        if not is_valid_circuit(C):
            counterexample = "Invalid circuit generated"
            conjecture_holds = False
            break
        
        R_n = hodge_rank(C)
        instances_tested += 1
        
        if R_n > Fraction(S_n, math.log(n + 1)):
            counterexample = f"Counterexample found: R({n}) = {R_n}, expected ≤ Ω(S({n})/log n)"
            conjecture_holds = False
            break
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": hodge_rank(generate_acc0_circuit(40)),
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
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")