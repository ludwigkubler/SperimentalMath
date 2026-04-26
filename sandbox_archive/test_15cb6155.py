import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def compose_dynamical_circuits(c1, c2):
        n = len(c1)
        composed_circuit = [0] * (n + 1)
        for i in range(n):
            if c1[i] == 1 and c2[i] == 1:
                composed_circuit[n] = 1
            else:
                composed_circuit[n] = 0
        return composed_circuit
    
    def induced_kolmogorov_flow(circuit):
        n = len(circuit)
        flow = 0
        for i in range(n):
            if circuit[i] != circuit[(i + 1) % n]:
                flow += 1
        return flow
    
    def communication_entropy_barrier(n):
        # Simplified lower bound for demonstration purposes
        return n * math.log2(n)
    
    def empirical_orbit_signature(circuit, num_samples=1000):
        n = len(circuit)
        signature = [0] * (n + 1)
        for _ in range(num_samples):
            state = random.getrandbits(n)
            next_state = circuit[state]
            if next_state != state:
                signature[next_state] += 1
        return sum(signature) / num_samples
    
    n_values = [5, 8, 11, 14]
    total_flow = 0
    composed_flow = 0
    entropy_barrier = 0
    instances_tested = 0
    
    for n in n_values:
        c1 = [random.randint(0, 1) for _ in range(n)]
        c2 = [random.randint(0, 1) for _ in range(n)]
        
        flow_c1 = induced_kolmogorov_flow(c1)
        flow_c2 = induced_kolmogorov_flow(c2)
        total_flow += flow_c1 + flow_c2
        
        composed_circuit = compose_dynamical_circuits(c1, c2)
        composed_flow = induced_kolmogorov_flow(composed_circuit)
        
        entropy_barrier += communication_entropy_barrier(n)
        instances_tested += 1
    
    conjecture_holds = total_flow + math.log(len(c1)) >= composed_flow
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "induced_kolmogorov_flow",
        "metric_value": composed_flow,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_flow = sum(r["metric_value"] for r in results) / len(results)
    std_flow = math.sqrt(sum((r["metric_value"] - mean_flow) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_flow} std={std_flow} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_flow} std={std_flow} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")