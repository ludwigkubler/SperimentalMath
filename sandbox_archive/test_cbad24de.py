# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_circuit(n, d, s):
    gates = []
    for _ in range(s):
        if len(gates) < 2:
            gate_type = random.choice(['AND', 'OR', 'NOT', 'XOR'])
        else:
            gate_type = random.choice(['AND', 'OR', 'NOT', 'XOR', 'INPUT'])
        if gate_type == 'INPUT':
            inputs = [random.randint(0, n-1)]
        else:
            inputs = random.sample(range(len(gates)), min(2, len(gates)))
        gates.append((gate_type, inputs))
    return gates

def compute_truth_table(circuit, n):
    truth_table = {}
    for inputs in itertools.product([0, 1], repeat=n):
        input_values = list(inputs)
        for gate in circuit:
            gate_type, gate_inputs = gate
            if gate_type == 'INPUT':
                output = input_values[gate_inputs[0]]
            elif gate_type == 'AND':
                output = input_values[gate_inputs[0]] & input_values[gate_inputs[1]]
            elif gate_type == 'OR':
                output = input_values[gate_inputs[0]] | input_values[gate_inputs[1]]
            elif gate_type == 'NOT':
                output = 1 - input_values[gate_inputs[0]]
            elif gate_type == 'XOR':
                output = input_values[gate_inputs[0]] ^ input_values[gate_inputs[1]]
            input_values.append(output)
        truth_table[inputs] = input_values[-1]
    return truth_table

def compute_supports(circuit, n):
    supports = []
    for gate in circuit:
        gate_type, gate_inputs = gate
        if gate_type == 'INPUT':
            support = [gate_inputs[0]]
        else:
            support = []
            for i in gate_inputs:
                support.extend(supports[i])
            support = list(set(support))
        supports.append(support)
    return supports

def build_gate_conflict_graph(supports):
    graph = defaultdict(set)
    for i in range(len(supports)):
        for j in range(i+1, len(supports)):
            if set(supports[i]) & set(supports[j]):
                graph[i].add(j)
                graph[j].add(i)
    return graph

def is_independent_set(graph, S):
    for i in S:
        for j in S:
            if i != j and j in graph[i]:
                return False
    return True

def compute_tau(graph):
    tau = 0
    for k in range(1, len(graph)+1):
        for S in itertools.combinations(graph.keys(), k):
            if is_independent_set(graph, S):
                tau += (-1)**k
    return tau

def compute_agreement(truth_table, mod_q):
    agreement = 0
    for inputs in truth_table:
        x = sum(inputs) % mod_q
        if truth_table[inputs] == (x != 0):
            agreement += 1
    return agreement

def run_trial(seed):
    random.seed(seed)
    n = random.choice([6, 8, 10, 12])
    d = random.choice([2, 3, 4])
    s = random.choice([8, 12, 16, 20])

    circuit = generate_random_circuit(n, d, s)
    truth_table = compute_truth_table(circuit, n)
    supports = compute_supports(circuit, n)
    graph = build_gate_conflict_graph(supports)
    tau = compute_tau(graph)

    mod_q = random.choice([3, 5])
    agreement = compute_agreement(truth_table, mod_q)
    threshold = (3/4) * (2**n)

    predicted_bound = 2**(n / (10 * d**2)) - 1
    conjecture_holds = tau >= predicted_bound if agreement >= threshold else True

    counterexample = ""
    if not conjecture_holds and agreement >= threshold:
        counterexample = f"tau={tau} < {predicted_bound} for n={n}, d={d}, s={s}, mod_q={mod_q}"

    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_instances += result["instances_tested"]

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / len(seeds)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"] and result["counterexample"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")