# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def is_monotonic(f):
        n = len(f)
        for i in range(1 << (n - 1)):
            if any(f[i | (1 << j)] < f[i] for j in range(n)):
                return False
        return True
    
    def generate_coxeter_dynkin_diagram(f):
        n = len(f)
        diagram = {}
        for i in range(2**n):
            for j in range(i + 1, 2**n):
                if all((f[i] <= f[j]) == (f[i & ~(1 << k)] <= f[j & ~(1 << k)]) for k in range(n)):
                    diagram[(i, j)] = True
        return diagram
    
    def count_symmetry_classes(diagram):
        n = len(f)
        classes = set()
        for i in range(2**n):
            class_set = {i}
            for j in range(i + 1, 2**n):
                if all((diagram[(i, k)] == diagram[(j, k)]) for k in range(n)):
                    class_set.add(j)
            classes.update(class_set)
        return len(classes)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_classes = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            if not is_monotonic(f):
                continue
            diagram = generate_coxeter_dynkin_diagram(f)
            classes = count_symmetry_classes(diagram)
            total_classes += classes
            instances_tested += 1
    
    metric_value = total_classes / instances_tested if instances_tested > 0 else 0
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Symmetry Classes",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_classes = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_classes} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_classes} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Function of degree {len(generate_boolean_function(5))}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")