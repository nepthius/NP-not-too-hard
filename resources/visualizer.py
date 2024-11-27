import matplotlib.pyplot as plt
import numpy as np

def visualize_task_results(results: dict, title: str = "Task Results"):
    """
    shows model results
    """

    #going through tasks and results
    tasks = list(results.keys())
    metrics = list(results.values())
    plt.figure(figsize=(10, 6))
    bars = plt.bar(tasks, metrics, color='skyblue', edgecolor='black')
    for bar, metric in zip(bars, metrics):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{metric:.2f}',
                 ha='center', va='bottom', fontsize=10)

    #plotting of resUlts
    plt.title(title, fontsize=16)
    plt.xlabel("Tasks", fontsize=14)
    plt.ylabel("Performance Metric", fontsize=14)
    plt.ylim(0, 1.1)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    #testing
    sample_results = {
        "Abbreviation Recognition": 0.85,
        "Definition Recognition": 0.92,
        "Named Entity Recognition": 0.78,
        "Question Answering": 0.88,
        "Link Retrieval": 0.94,
        "Certificate Question": 0.81,
        "XBRL Analytics": 0.76,
        "Common Domain Model": 0.89,
        "Model Openness Framework": 0.83
    }

    visualize_task_results(sample_results, title="MODELING!!!!!!!")