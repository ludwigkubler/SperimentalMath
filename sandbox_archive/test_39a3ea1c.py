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
    
    # Generate a random boolean circuit with up to 40 inputs
    n = random.randint(5, 30)
    circuit = [[random.choice([0, 1]) for _ in range(n)] for _ in range(random.randint(2, 10))]
    
    # Compute the graphical regularity of the circuit
    def is_planar(graph):
        if len(graph) <= 4:
            return True
        v = next(v for v in graph if len(graph[v]) > 3)
        neighbors = [u for u in graph if u != v and v in graph[u]]
        subgraph = {u: set() for u in neighbors}
        for u, v in graph.items():
            if u == v:
                continue
            for w in v:
                if w in neighbors:
                    subgraph[w].add(u)
        return is_planar(subgraph)
    
    def graphical_regularity(circuit):
        n = len(circuit[0])
        graph = {i: set() for i in range(n)}
        for gate in circuit:
            for i, lit in enumerate(gate):
                if lit == 1:
                    for j in range(i + 1, n):
                        if circuit[j][i] == 1 and circuit[i][j] == 1:
                            graph[i].add(j)
                            graph[j].add(i)
        return sum(len(graph[v]) for v in graph) / (2 * len(graph))
    
    gamma = graphical_regularity(circuit)
    
    # Simulate an n-party communication protocol that computes the OR function on the circuit's outputs
    def or_protocol(circuit):
        n = len(circuit[0])
        rank_variance = 0
        for _ in range(10):  # Repeat the protocol multiple times to get a good estimate
            inputs = [random.choice([0, 1]) for _ in range(n)]
            outputs = [any(gate[i] == 1 for gate in circuit) for i in range(n)]
            rank_variance += sum(outputs.count(1))
        return rank_variance / n
    
    rho_n = or_protocol(circuit)
    
    # Compare the graphical regularity to the rank variance
    metric_name = "graphical_regularity_to_rank_variance_ratio"
    metric_value = gamma / rho_n if rho_n != 0 else float('inf')
    instances_tested = 10
    n_max = n
    conjecture_holds = abs(gamma - rho_n) <= 1
    counterexample = "" if conjecture_holds else "graphical_regularity_not_close_to_rank_variance"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"graphical_regularity_not_close_to_rank_variance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")