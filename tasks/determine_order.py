import logging
import networkx as nx
import json
import os

def determine_creation_order(foreign_keys):
    graph = nx.DiGraph()

    # Add nodes for each table
    tables = foreign_keys.keys()
    graph.add_nodes_from(tables)

    # Add edges based on foreign key relationships
    for table, refs in foreign_keys.items():
        for ref in refs:
            graph.add_edge(ref, table)

    # Perform topological sort
    try:
        creation_order = list(nx.topological_sort(graph))
        logging.info("Order of table creation:")
        for table in creation_order:
            logging.info(table)
        return creation_order
    except nx.NetworkXUnfeasible:
        logging.error("Graph is not acyclic. There is a cycle in the graph.")
        return None

def run(foreign_keys_file):
    logging.info(f"Determining order of table creation from foreign keys file: {foreign_keys_file}")

    try:
        with open(foreign_keys_file, 'r') as file:
            foreign_keys = json.load(file)

        creation_order = determine_creation_order(foreign_keys)

        if creation_order:
            base_name = os.path.splitext(os.path.basename(foreign_keys_file))[0]
            output_file = f"{base_name}_table_creation_order.txt"
            with open(output_file, 'w') as f:
                for table in creation_order:
                    f.write(table + "\n")
            logging.info(f"Order of table creation written to {output_file}")

    except FileNotFoundError:
        logging.error(f"File {foreign_keys_file} not found.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    foreign_keys_file = "foreign_keys.json"
    run(foreign_keys_file)
