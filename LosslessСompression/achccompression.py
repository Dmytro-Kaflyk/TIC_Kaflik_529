import matplotlib.pyplot as plt

def plot_results_table(results, N):
    git
    checkout - b
    LessСompressionJPEG

    fig, ax = plt.subplots(figsize=(14/1.54, N/1.54))
    headers = ['Ентропія', 'bps AC', 'bps CH']
    rows = [f'Послідовність {i+1}' for i in range(N)]

    ax.axis('off')

    table = ax.table(cellText=results,
                     colLabels=headers,
                     rowLabels=rows,
                     loc='center',
                     cellLoc='center')

    table.set_fontsize(14)
    table.scale(0.8, 2)

    fig.savefig("Результати_стиснення_методами_AC_та_CH.png")
    plt.show()

results = [
    [3.15, 1.05, 1.12],
    [2.87, 1.22, 1.19],
    [3.05, 1.08, 1.10],
    [2.95, 1.15, 1.20],
    [3.10, 1.07, 1.14],
    [2.90, 1.10, 1.16],
    [3.00, 1.12, 1.18],
    [2.85, 1.20, 1.22],
]

N = len(results)
plot_results_table(results, N)
