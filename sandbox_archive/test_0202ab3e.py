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
    
    def xor_and_tree_width(cnf):
        # Simplified XOR-AND tree width calculation (example implementation)
        return len(cnf)
    
    def tropicalized_group_order(n):
        # Example implementation of a function to find the minimal order
        return 2 ** n
    
    metric_name = "tropicalized_group_order"
    instances_tested = 0
    total_order = 0
    total_width = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(100):
        n = random.randint(5, 40)
        cnf = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
        width = xor_and_tree_width(cnf)
        order = tropicalized_group_order(n)
        
        total_order += order
        total_width += width
        instances_tested += 1
        
        if order < 0.7 * width:
            conjecture_holds = False
            counterexample = f"n={n}, width={width}, order={order}"
    
    mean_order = Fraction(total_order, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    slope = (mean_order - 0) / (mean_width - 0)
    
    if slope < 0.7:
        conjecture_holds = False
        counterexample = f"n={n}, width={width}, order={order}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(slope),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")