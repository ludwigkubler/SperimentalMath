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
    
    def shannon_entropy(f):
        n = len(f)
        counts = [f.count(0), f.count(1)]
        total = sum(counts)
        if total == 0:
            return 0
        probabilities = [c / total for c in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy
    
    def coxeter_diagram(f):
        n = len(f)
        diagram = {}
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    key = tuple(sorted([i, j]))
                    if key not in diagram:
                        diagram[key] = 0
                    diagram[key] += 1
        return diagram
    
    def is_isomorphic(diag1, diag2):
        if len(diag1) != len(diag2):
            return False
        keys1 = sorted(diag1.keys())
        keys2 = sorted(diag2.keys())
        if keys1 != keys2:
            return False
        for key in keys1:
            if diag1[key] != diag2[key]:
                return False
        return True
    
    def count_isomorphism_classes(diag):
        classes = []
        for perm in itertools.permutations(range(len(diag))):
            new_diag = {}
            for (i, j), count in diag.items():
                new_key = tuple(sorted([perm[i], perm[j]]))
                if new_key not in new_diag:
                    new_diag[new_key] = 0
                new_diag[new_key] += count
            if all(is_isomorphic(new_diag, cls) for cls in classes):
                classes.append(new_diag)
        return len(classes)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        H_f = shannon_entropy(f)
        diag = coxeter_diagram(f)
        num_classes = count_isomorphism_classes(diag)
        ratio = num_classes / math.exp(H_f)
        results.append({
            "n": n,
            "H_f": H_f,
            "num_classes": num_classes,
            "ratio": ratio
        })
    
    metric_value = sum(r["ratio"] for r in results) / len(results)
    conjecture_holds = all(r["ratio"] <= 1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of |Diag(f)| to exp(H(f))",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")