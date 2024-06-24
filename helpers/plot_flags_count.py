import matplotlib.pyplot as plt

# Function to plot flags count
def plot_flags_count(df, flag_columns, fcs_flags, output_file):
    plot_hh_summary = df[flag_columns].sum()
    sorted_sum = plot_hh_summary.sort_values(ascending=False)
    sorted_sum.index = [fcs_flags.get(label, label) for label in sorted_sum.index]

    plt.figure(figsize=(12, 6))
    bars = plt.barh(sorted_sum.index, sorted_sum.values, color='royalblue')
    plt.gca().invert_yaxis()
    for bar in bars:
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', ha='left', va='center', color='black', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file)
    plt.show()