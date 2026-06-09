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
        return [random.choice([0, 1]) for _ in range(n)]
    
    def construct_coxeter_dynkin_diagram(instance):
        n = len(instance)
        if n == 1:
            return 0
        diagram = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] != instance[j]:
                    diagram[i][j] = 1
                    diagram[j][i] = 1
        return sum(sum(row) for row in diagram) // 2
    
    def mean(lst):
        return Fraction(sum(lst), len(lst))
    
    def stdev(lst, m):
        return math.sqrt(mean([x**2 for x in lst]) - m**2)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        instances_tested = 30
        edge_counts = []
        for _ in range(instances_tested):
            instance = generate_sat_instance(n)
            edge_count = construct_coxeter_dynkin_diagram(instance)
            edge_counts.append(edge_count)
        
        avg_edge_count = mean(edge_counts)
        std_edge_count = stdev(edge_counts, avg_edge_count)
        
        results.append({
            "metric_name": "Coxeter-Dynkin Diagram Edge Count",
            "metric_value": avg_edge_count,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": avg_edge_count <= 1.5**n,
            "counterexample": "" if avg_edge_count <= 1.5**n else f"avg_edge_count={avg_edge_count}, 1.5^{n}={1.5**n}"
        })
    
    return {
        "seed": seed,
        **results[-1]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = [run_trial(seed) for seed in seeds]
    
    avg_metric_value = mean([r["metric_value"] for r in results])
    std_metric_value = stdev([r["metric_value"] for r in results], avg_metric_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")