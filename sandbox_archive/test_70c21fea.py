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
    
    def tseitin_circuit(n):
        if n == 1:
            return "x"
        else:
            x = f"x{n}"
            y = f"y{n}"
            z = f"z{n}"
            subformula = f"{tseitin_circuit(n-1)} & ~{z} | {y} & ~{z} | ~{y} & ~{x}"
            return subformula
    
    def frege_proof_width(formula):
        if formula.startswith("x"):
            return 1
        elif formula.startswith("("):
            left, op, right = formula[1:-1].split()
            return max(frege_proof_width(left), frege_proof_width(right)) + 1
        else:
            raise ValueError("Invalid formula")
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = tseitin_circuit(n)
        width = frege_proof_width(formula)
        results.append((n, width))
    
    if not results:
        return {
            "metric_name": "frege_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, widths = zip(*results)
    mean_width = sum(widths) / len(widths)
    std_width = math.sqrt(sum((w - mean_width) ** 2 for w in widths) / len(widths))
    
    support_fraction = sum(1 for w in widths if abs(w - math.log(n, 2)) <= 0.1 * math.log(n, 2)) / len(widths)
    
    return {
        "metric_name": "frege_proof_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")