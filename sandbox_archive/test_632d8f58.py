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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def monomial_complexity(n):
        return n
    
    def compute_grobner_basis_size(n):
        # Simplified approximation
        return 2**n
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    I_F = set()
    for i in range(1 << n):
        if all(formula[i >> j] == '1' for j in range(n) if (i & (1 << j))):
            monomial = tuple(i >> j for j in range(n))
            I_F.add(monomial)
    
    quotient_sheaf_rank = len(I_F)
    gamma_n = monomial_complexity(n)
    grobner_basis_size = compute_grobner_basis_size(n)
    
    metric_value = quotient_sheaf_rank / grobner_basis_size
    conjecture_holds = quotient_sheaf_rank <= gamma_n
    counterexample = "" if conjecture_holds else f"n={n}, ρ(I_F)={quotient_sheaf_rank}, γ(n)={gamma_n}"
    
    return {
        "metric_name": "Quotient Sheaf Rank / Gröbner Basis Size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, ρ(I_F)={results[first_failing_seed]['metric_value']}, γ(n)={monomial_complexity(results[first_failing_seed]['instances_tested'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")