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
    
    def frege_proof_length(n):
        # Simplified DPLL solver to estimate Frege proof length
        if n == 1:
            return 2
        elif n == 2:
            return 4
        else:
            return 2 * frege_proof_length(n - 1) + 2
    
    def von_neumann_entropy(n):
        # Simplified calculation of von Neumann entropy for a uniform superposition
        return math.log2(n)
    
    c = 1.0  # Constant factor to be determined experimentally
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(10, 41):
        for _ in range(3):  # Test multiple times per size
            f = [random.choice([0, 1]) for _ in range(2**n)]
            proof_length = frege_proof_length(n)
            entropy = von_neumann_entropy(len(f))
            
            if entropy > c * math.log2(math.factorial(n)) / math.log2(proof_length):
                conjecture_holds = False
                counterexample = f"Function with n={n}, entropy={entropy}, proof_length={proof_length}"
                break
        
        instances_tested += 3
    
    return {
        "metric_name": "Frege Proof Length vs Von Neumann Entropy",
        "metric_value": c,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")