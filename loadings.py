import matplotlib.pyplot as plt

plt.clf()
plt.title('Loadins')
for d in in_datas:
    for _i, _p in enumerate(d.X[:,0:2],start=1):
        _x, _y = _p
        # Vetores vermelhos partindo da origem (0,0)
        plt.arrow(0, 0, _x, _y, color='crimson', head_width=0.04, head_length=0.04, linewidth=2, length_includes_head=True)
        # Texto identificando a variável original
        plt.text(_x*1.05,_y*1.05,f'{_i}', color='crimson', ha='center', va='center', fontsize=11, fontweight='bold')

plt.show()
