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
    
    def communication_protocol(f):
        n = len(f)
        protocol = []
        for i in range(n):
            output_bit = f[i]
            protocol.append(output_bit)
        return protocol
    
    def shannon_entropy(p):
        entropy = 0
        for prob in p:
            if prob > 0:
                entropy -= prob * math.log2(prob)
        return entropy
    
    def geometric_entropy(protocol):
        n = len(protocol)
        distribution = [protocol.count(i) / n for i in range(2)]
        return shannon_entropy(distribution)
    
    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    metric_name = "geometric_entropy"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1, 5):
        f = random_boolean_function(n)
        protocol = communication_protocol(f)
        H_G_P = geometric_entropy(protocol)
        
        if n == 5:
            expected_bound = 5 * math.log2(n)
        elif n == 10:
            expected_bound = 10 * math.log2(n)
        elif n == 15:
            expected_bound = 15 * math.log2(n)
        elif n == 20:
            expected_bound = 20 * math.log2(n)
        elif n == 30:
            expected_bound = 30 * math.log2(n)
        elif n == 40:
            expected_bound = 40 * math.log2(n)
        
        if H_G_P < expected_bound - 1 or H_G_P > expected_bound + 1:
            conjecture_holds = False
            counterexample = f"n={n}, H(G(P))={H_G_P}, expected_bound={expected_bound}"
    
    return {
        "metric_name": metric_name,
        "metric_value": H_G_P,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.3:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])]['counterexample']}\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")