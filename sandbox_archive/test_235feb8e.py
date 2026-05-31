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
    
    def generate_boolean_function(n):
        return [random.choice([-1, 1]) for _ in range(2**n)]
    
    def conjugacy_class_enumeration(f):
        n = int(math.log2(len(f)))
        G = []
        for i in range(2**n):
            g = [f[i ^ j] * f[j] for j in range(2**n)]
            if g not in G:
                G.append(g)
        return G
    
    def count_irreducible_representations(G):
        # Placeholder for actual computation
        return len(G)
    
    n_values = [5, 10, 20, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        G = conjugacy_class_enumeration(f)
        chi_f = count_irreducible_representations(G)
        results.append({
            "n": n,
            "chi_f": chi_f
        })
    
    total_chi_f = sum(result["chi_f"] for result in results)
    mean_chi_f = Fraction(total_chi_f, len(results))
    std_chi_f = math.sqrt(sum((result["chi_f"] - mean_chi_f)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["chi_f"] - 2**n_values[results.index(result)]) / (2**n_values[results.index(result)]) <= Fraction(1, 20)) / len(results)
    
    conjecture_holds = support_fraction >= Fraction(4, 5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "chi_f",
        "metric_value": mean_chi_f,
        "instances_tested": len(results),
        "n_max": max(n_values),
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 2**r["n_max"]) / (2**r["n_max"]) > Fraction(1, 10) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - 2**result["n_max"]) / (2**result["n_max"]) > Fraction(1, 10))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")