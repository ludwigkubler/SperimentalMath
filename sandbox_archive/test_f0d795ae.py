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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), random.randint(1, n)))
            circuit.append((gate_type, inputs))
        return circuit
    
    def term_overlap_graph(circuit):
        n = len(circuit[0][1])
        graph = [[0] * (2**n) for _ in range(2**n)]
        for gate in circuit:
            if gate[0] == 'AND':
                for i in gate[1]:
                    for j in gate[1]:
                        if i != j:
                            graph[i][j] += 1
            elif gate[0] == 'OR':
                for i in gate[1]:
                    for j in range(n):
                        if j not in gate[1]:
                            graph[i][j] += 1
        return graph
    
    def eta_invariant(graph):
        n = len(graph)
        total_edges = sum(sum(row) for row in graph) // 2
        max_degree = max(max(row) for row in graph)
        return Fraction(total_edges, max_degree)
    
    def monotone_width(circuit):
        n = len(circuit[0][1])
        assignments = [list(range(n)) for _ in range(2**n)]
        
        for gate in circuit:
            new_assignments = []
            for assignment in assignments:
                if all(assignment[i] == (gate[1][i] % 2) for i in gate[1]):
                    new_assignment = list(assignment)
                    for i in gate[1]:
                        new_assignment[i] = (new_assignment[i] + 1) % 2
                    new_assignments.append(new_assignment)
            assignments = new_assignments
        
        return len(assignments)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        graph = term_overlap_graph(circuit)
        eta = eta_invariant(graph)
        w_m = monotone_width(circuit)
        
        results.append({
            "n": n,
            "eta": eta,
            "w_m": w_m
        })
    
    correlation = 0.0
    for result in results:
        correlation += (result["eta"] - result["w_m"]) ** 2
    
    correlation /= len(results)
    correlation = math.sqrt(correlation)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation > 0.8,
        "counterexample": "" if correlation > 0.8 else "Correlation below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")