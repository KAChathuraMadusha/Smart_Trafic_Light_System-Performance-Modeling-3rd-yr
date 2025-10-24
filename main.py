import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------
# Smart Traffic Light Simulation
# --------------------------

# Vehicle arrival process
def vehicle_arrival(env, intersection, arrival_rate, service_time, results, strategy):
    while True:
        yield env.timeout(random.expovariate(1 / arrival_rate))
        env.process(vehicle(env, intersection, service_time, results, strategy))

# Vehicle process
def vehicle(env, intersection, service_time, results, strategy):
    arrival_time = env.now
    with intersection.request() as request:
        yield request
        wait_time = env.now - arrival_time
        yield env.timeout(random.expovariate(1 / service_time))
        results["wait_times"].append(wait_time)
        results["throughput"].append(1)
        results["vehicles_served"] += 1

# Simulation function
def run_simulation(arrival_rate, service_time, capacity, strategy):
    env = simpy.Environment()
    intersection = simpy.Resource(env, capacity=capacity)
    results = {"wait_times": [], "throughput": [], "vehicles_served": 0}

    # Adaptive strategy adjusts service time
    if strategy == "Adaptive":
        service_time *= 0.8

    env.process(vehicle_arrival(env, intersection, arrival_rate, service_time, results, strategy))
    env.run(until=3600)  # 1 hour

    avg_wait = sum(results["wait_times"]) / len(results["wait_times"]) if results["wait_times"] else 0
    throughput = sum(results["throughput"]) / 3600

    return {
        "Arrival Rate": arrival_rate,
        "Service Time": service_time,
        "Capacity": capacity,
        "Strategy": strategy,
        "Avg_Wait(s)": round(avg_wait, 2),
        "Throughput": round(throughput, 2),
        "Vehicles_Served": results["vehicles_served"]
    }

# --------------------------
# Run Experiments with User Input
# --------------------------

def run_experiments():
    print("\n--- SMART TRAFFIC LIGHT SIMULATION ---")
    all_results = []

    num_experiments = int(input("Enter number of experiments to run: "))

    for i in range(num_experiments):
        print(f"\nExperiment {i+1}:")

        # Get user inputs
        while True:
            try:
                arrival_rate = float(input("Enter vehicle arrival rate (seconds between arrivals, e.g., 10): "))
                if arrival_rate <= 0:
                    raise ValueError
                break
            except ValueError:
                print("⚠️ Enter a positive number!")

        while True:
            try:
                service_time = float(input("Enter average service time (seconds per vehicle, e.g., 5): "))
                if service_time <= 0:
                    raise ValueError
                break
            except ValueError:
                print("⚠️ Enter a positive number!")

        while True:
            try:
                capacity = int(input("Enter number of lanes (1–3): "))
                if capacity not in [1, 2, 3]:
                    raise ValueError
                break
            except ValueError:
                print("⚠️ Enter 1, 2, or 3!")

        while True:
            strategy = input("Enter strategy (Fixed/Adaptive): ").capitalize()
            if strategy in ["Fixed", "Adaptive"]:
                break
            print("⚠️ Strategy must be 'Fixed' or 'Adaptive'!")

        result = run_simulation(arrival_rate, service_time, capacity, strategy)
        all_results.append(result)

    # Convert results to DataFrame
    results_df = pd.DataFrame(all_results)
    print("\nSimulation Results:\n", results_df)

    # --------------------------
    # Visualization Section
    # --------------------------
    os.makedirs("visualizations", exist_ok=True)

    # Average Wait Time Chart
    plt.figure(figsize=(8, 5))
    plt.title("Average Wait Time per Experiment")
    plt.bar(range(len(results_df)), results_df["Avg_Wait(s)"])
    plt.xticks(range(len(results_df)), [f"Exp {i+1}" for i in range(len(results_df))])
    plt.ylabel("Average Wait Time (s)")
    plt.tight_layout()
    plt.savefig("visualizations/wait_times_comparison.png")
    plt.close()

    # Throughput Chart
    plt.figure(figsize=(8, 5))
    plt.title("Throughput per Experiment")
    plt.bar(range(len(results_df)), results_df["Throughput"])
    plt.xticks(range(len(results_df)), [f"Exp {i+1}" for i in range(len(results_df))])
    plt.ylabel("Throughput (vehicles/sec)")
    plt.tight_layout()
    plt.savefig("visualizations/throughput_comparison.png")
    plt.close()

    # Vehicles Served Chart
    plt.figure(figsize=(8, 5))
    plt.title("Vehicles Served per Experiment")
    plt.bar(range(len(results_df)), results_df["Vehicles_Served"])
    plt.xticks(range(len(results_df)), [f"Exp {i+1}" for i in range(len(results_df))])
    plt.ylabel("Vehicles Served (per hour)")
    plt.tight_layout()
    plt.savefig("visualizations/vehicles_served_comparison.png")
    plt.close()

    print("\n✅ All visualizations saved in the 'visualizations' folder successfully!")
    return results_df

# --------------------------
# Main
# --------------------------
if __name__ == "__main__":
    run_experiments()

