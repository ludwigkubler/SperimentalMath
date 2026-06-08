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
    
    def generate_bit_sequence(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def indicator_function(sequence):
        return sequence
    
    def p_adic_divergence(f1, f2):
        n = len(f1)
        divergence = 0
        for i in range(n):
            if f1[i] != f2[i]:
                divergence += math.log(1 / (i + 1), 2)
        return divergence
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, m):
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    divergences = []
    
    for n in n_values:
        f1 = indicator_function(generate_bit_sequence(n))
        f2 = indicator_function(generate_bit_sequence(n))
        divergence = p_adic_divergence(f1, f2)
        divergences.append(divergence)
    
    mean_divergence = mean(divergences)
    std_deviation = std(divergences, mean_divergence)
    support_fraction = len([d for d in divergences if d <= math.log2(n)]) / len(divergences)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mean_divergence > log2(n)"
    
    return {
        "metric_name": "p-adic divergence",
        "metric_value": mean_divergence,
        "instances_tested": len(divergences),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = std([r["metric_value"] for r in results], mean_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_divergence > log2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")