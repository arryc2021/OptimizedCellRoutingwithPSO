import numpy as np
import random
import streamlit as st
import matplotlib.pyplot as plt
from pyswarm import pso

# Network environment setup
class NetworkEnvironment:
    def __init__(self, num_nodes=10, max_range=10):
        self.num_nodes = num_nodes
        self.max_range = max_range
        self.nodes = np.random.rand(self.num_nodes, 2) * self.max_range  # Randomized positions of nodes

    def get_distance(self, node1, node2):
        return np.linalg.norm(self.nodes[node1] - self.nodes[node2])

    def network_reliability(self, path):
        # Simulate call drops based on path distance and connectivity.
        total_distance = sum([self.get_distance(path[i], path[i+1]) for i in range(len(path)-1)])
        # Fitness is higher for shorter paths with fewer hops
        return -total_distance  # Negative because PSO minimizes the objective function.

    def visualize_network(self, path=None):
        plt.scatter(self.nodes[:, 0], self.nodes[:, 1], c='blue', label='Nodes')
        if path is not None:
            for i in range(len(path)-1):
                plt.plot([self.nodes[path[i], 0], self.nodes[path[i+1], 0]], 
                         [self.nodes[path[i], 1], self.nodes[path[i+1], 1]], 'r-', linewidth=2)
        plt.title("Network Visualization")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.show()

# PSO Algorithm for routing
def pso_routing(network: NetworkEnvironment):
    def fitness_function(x):
        path = list(map(int, x))  # Convert continuous path to integer indices
        return -network.network_reliability(path)
    
    lb = [0] * (network.num_nodes - 1)  # Lower bounds (start node indices)
    ub = [network.num_nodes - 1] * (network.num_nodes - 1)  # Upper bounds (end node indices)
    
    # Run PSO for routing optimization
    xopt, _ = pso(fitness_function, lb, ub, swarmsize=50, maxiter=100)
    return list(map(int, xopt))  # Return optimal path

# Streamlit UI
def run_simulation():
    st.title("Network Routing Simulation with PSO")
    
    # Initialize Network
    num_nodes = st.slider("Number of Network Nodes", 5, 20, 10)
    max_range = st.slider("Max Range of Network (X, Y)", 5, 20, 10)
    network = NetworkEnvironment(num_nodes=num_nodes, max_range=max_range)

    # Visualize Network Nodes
    network.visualize_network()
    st.pyplot(plt)

    # Run PSO for routing
    if st.button("Optimize Network Routing"):
        optimized_path = pso_routing(network)
        st.write(f"Optimized Path: {optimized_path}")
        
        # Visualize Optimized Path
        network.visualize_network(optimized_path)
        st.pyplot(plt)

if __name__ == "__main__":
    run_simulation()
