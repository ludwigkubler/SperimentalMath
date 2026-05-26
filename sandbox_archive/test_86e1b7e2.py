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
    
    def generate_sat_instance(n):
        return [random.choice(['0', '1']) for _ in range(2**n)]
    
    def tseitin_resolution_width(sat_instance):
        n = len(sat_instance)
        clauses = []
        for i in range(n):
            clauses.append([i])
            clauses.append([-i - 1])
        return n + 1
    
    def algebraic_curvature(n):
        # Simplified model of algebraic curvature
        return Fraction(1, n**2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    curvatures = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        width = tseitin_resolution_width(sat_instance)
        curvature = algebraic_curvature(n)
        widths.append(width)
        curvatures.append(curvature)
    
    correlation_coefficient = sum((w - mean_w) * (c - mean_c) for w, c in zip(widths, curvatures)) / (len(widths) * std_w * std_c)
    mean_w = sum(widths) / len(widths)
    mean_c = sum(curvatures) / len(curvatures)
    std_w = math.sqrt(sum((w - mean_w)**2 for w in widths) / len(widths))
    std_c = math.sqrt(sum((c - mean_c)**2 for c in curvatures) / len(curvatures))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(c - mean_c) <= 3 * std_c for c in curvatures),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 or abs(c - mean_c) > 3 * std_c for c, mean_c, std_c in zip(curvatures, [mean_c] * len(curvatures), [std_c] * len(curvatures))):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data n_tested={len(seeds)}")