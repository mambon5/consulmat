import matplotlib.pyplot as plt

# Datos
non_compliant_requirements = [0, 1, 2, 3, 4, 5, 6, 7, 8]
brp_counts = [0, 2, 3, 5, 4, 5, 6, 2, 1]
brp_percentages = [0, 7, 11, 18, 14, 18, 21, 7, 4]  # En porcentaje

# Crear figura
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar barras
bars = ax.bar(
    non_compliant_requirements,
    brp_counts,
    width=0.6,
    color='#A7C7E7',
    edgecolor='gray',
    linewidth=1
)

# Etiquetas de ejes (sin título)
ax.set_xlabel(
    'Number of non-compliant requirements',
    fontsize=14,
    fontname='Times New Roman'
)
ax.set_ylabel(
    'Number of BRP',
    fontsize=14,
    fontname='Times New Roman'
)

# Limite del eje Y
ax.set_ylim(0, 7)

# Etiquetas de porcentaje sobre cada barra
for bar, pct in zip(bars, brp_percentages):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.2,
        f'{pct}%',
        ha='center',
        va='bottom',
        fontsize=12,
        fontname='Times New Roman'
    )

# Personalizar ejes
ax.set_xticks(sorted(set(non_compliant_requirements)))
ax.set_xticklabels(
    sorted(set(non_compliant_requirements)),
    fontname='Times New Roman',
    fontsize=12
)
ax.set_yticks(range(0, 7, 1))
ax.set_yticklabels(
    [str(i) for i in range(0, 7)],
    fontname='Times New Roman',
    fontsize=12
)

# Cuadrícula sutil
ax.yaxis.grid(True, linestyle='--', alpha=0.4)

# Ocultar spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_bounds(0,6)
ax.tick_params(axis='y', which='both', right=False)

# Ajustar márgenes
plt.tight_layout()

plt.show()
