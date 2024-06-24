import matplotlib.pyplot as plt

# Function to plot error percentage by enumerator
def plot_error_percentage(summary_df, output_file):
    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(summary_df)), summary_df['Error_Percentage'], color='royalblue')
    plt.yticks(range(len(summary_df)), summary_df['EnuName'])
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.01, i, f'{bar.get_width() * 100:.1f}%', ha='left', va='center', color='black', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()