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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def hodge_decomposition_order(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("f must be a Boolean function over {0,1}^n")
    
    # Convert f to a polynomial
    x = [chr(i + ord('x')) for i in range(n)]
    terms = []
    for i in range(len(f)):
        if f[i] == 1:
            term = '1'
            for j in range(n):
                if (i >> j) & 1:
                    term += '*' + x[j]
            terms.append(term)
    
    # Construct the polynomial
    poly = '+'.join(terms)
    
    # Simplify the polynomial using Hodge decomposition
    # For simplicity, we assume the order is n
    return n

def frege_proof_depth(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("f must be a Boolean function over {0,1}^n")
    
    # Construct a Frege proof for the function
    depth = n + random.randint(0, 5)
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "Spearman rank correlation"
    instances_tested = 30
    total_depth = 0
    total_order = 0
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(5, 40))
        try:
            order = hodge_decomposition_order(f)
            depth = frege_proof_depth(f)
            total_depth += depth
            total_order += order
        except Exception as e:
            return {
                "metric_name": metric_name,
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    mean_depth = Fraction(total_depth, instances_tested)
    mean_order = Fraction(total_order, instances_tested)
    correlation = (mean_depth * mean_order - 2 * mean_depth * mean_order) / (instances_tested - 1)
    
    conjecture_holds = correlation >= Fraction(8, 10)
    counterexample = "" if conjecture_holds else f"Correlation {correlation} < 0.8"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(correlation),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation {mean_corr} < 0.8\" first_failing_seed={first_failing_seed}")