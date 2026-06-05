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
    
    def generate_circuit(n):
        circuit = {}
        for i in range(2**n):
            circuit[i] = [random.choice([0, 1]) if j == n else None for j in range(n+1)]
        return circuit
    
    def topological_entropy(circuit):
        n = len(circuit)
        visited = [False] * n
        entropy = 0
        
        def dfs(node):
            nonlocal entropy
            if visited[node]:
                return 0
            visited[node] = True
            children = [child for child, inputs in circuit.items() if inputs[0] == node]
            entropy += math.log(len(children))
            for child in children:
                entropy += dfs(child)
            return entropy
        
        for i in range(n):
            if not visited[i]:
                entropy += dfs(i)
        
        return entropy / n
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    
    entropy = topological_entropy(circuit)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": entropy <= 2**n,
        "counterexample": "" if entropy <= 2**n else f"Entropy {entropy} exceeds bound 2^{n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")