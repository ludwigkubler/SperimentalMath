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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def syntactic_monoid_generators(f):
        n = len(f)
        generators = []
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    continue
                new_f = [f[k] ^ (f[i] & f[j]) for k in range(2**n)]
                if new_f not in generators:
                    generators.append(new_f)
        return len(generators)
    
    def acc0_circuit_depth(f):
        n = len(f)
        depth = 1
        while True:
            new_f = [f[k] ^ (f[i] & f[j]) for i, j in itertools.combinations(range(n), 2)]
            if new_f == f:
                return depth
            f = new_f
            depth += 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    
    generators = syntactic_monoid_generators(f)
    circuit_depth = acc0_circuit_depth(f)
    
    metric_value = generators * math.log(n)
    conjecture_holds = (generators <= metric_value) and (circuit_depth >= 2**n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generators vs LogN",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")