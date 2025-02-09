import matplotlib.pyplot as plt
import networkx as nx

class PDA:
    def __init__(self, threshold):
        self.state = 'q0'  # Initial state
        self.stack = []  # Stack to track failed attempts
        self.threshold = threshold  # Number of failed attempts to trigger alert

    def transition(self, input_symbol):
        if self.state == 'q0':  # Initial state
            if input_symbol == 'F':
                self.stack.append('X')
                self.state = 'q1'
            elif input_symbol == 'S':
                self.state = 'q3'

        elif self.state == 'q1':  # Tracking state
            if input_symbol == 'F':
                self.stack.append('X')
                if len(self.stack) >= self.threshold:
                    self.state = 'q2'
            elif input_symbol == 'S':
                self.stack.clear()
                self.state = 'q3'

        elif self.state == 'q2':  # Alert state
            print("Alert: Brute-force attack detected!")
            self.state = 'q0'  # Reset after alert

        elif self.state == 'q3':  # Success state
            self.stack.clear()
            self.state = 'q0'  # Reset to initial state

    def reset(self):
        self.state = 'q0'
        self.stack.clear()

def test_pda():
    pda = PDA(threshold=3)
    # Test sequence of login attempts
    login_attempts = ['F', 'F', 'F', 'S', 'F', 'F', 'F', 'F']

    print("Processing login attempts...")
    for attempt in login_attempts:
        pda.transition(attempt)
        print(f"State: {pda.state}, Stack: {pda.stack}")

def visualize_pda():
    G = nx.DiGraph()
    states = ['q0 (Initial)', 'q1 (Tracking)', 'q2 (Alert)', 'q3 (Success)']
    G.add_nodes_from(states)

    transitions = [
        ('q0 (Initial)', 'q1 (Tracking)', 'F: Push X'),
        ('q1 (Tracking)', 'q1 (Tracking)', 'F: Push X'),
        ('q1 (Tracking)', 'q2 (Alert)', 'Threshold Reached'),
        ('q1 (Tracking)', 'q3 (Success)', 'S: Clear Stack'),
        ('q2 (Alert)', 'q0 (Initial)', 'Reset'),
        ('q3 (Success)', 'q0 (Initial)', 'Reset')
    ]
    for from_state, to_state, label in transitions:
        G.add_edge(from_state, to_state, label=label)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title("PDA Design for Detecting Brute-Force Login Attempts", fontsize=14)
    plt.show()

if __name__ == "__main__":
    test_pda()
    visualize_pda()