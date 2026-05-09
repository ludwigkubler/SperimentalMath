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
    
    def generate_pseudolines(n):
        pseudolines = []
        for i in range(n):
            x1, y1 = random.uniform(-1, 1), random.uniform(-1, 1)
            x2, y2 = random.uniform(-1, 1), random.uniform(-1, 1)
            if (x2 - x1) != 0:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                pseudolines.append((m, c))
        return pseudolines
    
    def compute_discrepancy(pseudolines):
        n = len(pseudolines)
        discrepancy = 0
        for i in range(n):
            for j in range(i + 1, n):
                m1, c1 = pseudolines[i]
                m2, c2 = pseudolines[j]
                if m1 != m2:
                    x = (c2 - c1) / (m1 - m2)
                    y1 = m1 * x + c1
                    y2 = m2 * x + c2
                    if abs(y1 - y2) > 1e-6:
                        discrepancy += 1
        return discrepancy
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    pseudolines = generate_pseudolines(n)
    discrepancy = compute_discrepancy(pseudolines)
    
    expected_discrepancy = 1 / math.log(n + 1)
    return {
        "metric_name": "discrepancy",
        "metric_value": discrepancy,
        "instances_tested": n * (n - 1) // 2,
        "conjecture_holds": abs(discrepancy - expected_discrepancy) < 0.1,
        "counterexample": "" if conjecture_holds else f"Discrepancy {discrepancy} does not match expected {expected_discrepancy}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_discrepancy = sum(r["metric_value"] for r in results) / len(results)
    std_discrepancy = math.sqrt(sum((r["metric_value"] - mean_discrepancy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_discrepancy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")