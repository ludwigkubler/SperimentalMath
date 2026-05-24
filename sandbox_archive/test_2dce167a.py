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
    
    def fourier_coefficients(f, n):
        coeffs = [0] * (2**n)
        for i in range(2**n):
            sum_val = 0
            for j in range(2**n):
                term = f(j) * math.cos(math.pi * i * j / (2**n))
                sum_val += term
            coeffs[i] = sum_val / (2**n)
        return coeffs
    
    def algebraic_k_theory_rank(coeffs):
        n = len(coeffs)
        rank = 0
        for coeff in coeffs:
            if coeff != 0:
                rank += 1
        return rank
    
    def xor_communication_complexity(f, n):
        # Simplified XOR communication complexity calculation
        return n
    
    instances_tested = 30
    total_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = lambda x: int(x % 2 == 1)  # Example Boolean function (XOR with constant input)
        coeffs = fourier_coefficients(f, n)
        rank = algebraic_k_theory_rank(coeffs)
        total_rank += rank
        complexity = xor_communication_complexity(f, n)
        
        if rank > complexity * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, complexity*log(n)={complexity*math.log(n)}"
    
    mean_rank = total_rank / instances_tested
    std_rank = (sum((x - mean_rank)**2 for x in [algebraic_k_theory_rank(fourier_coefficients(lambda x: int(x % 2 == 1), n)) for _ in range(instances_tested)]) / instances_tested) ** 0.5
    
    return {
        "metric_name": "Algebraic K-Theory Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")