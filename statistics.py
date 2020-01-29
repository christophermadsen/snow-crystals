import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

# scatter plots
outcomes = pd.read_csv('statisticaloutcomes.csv')
area = np.array(outcomes['frozen_area']).reshape(-1, 1)
beta = np.array(outcomes['beta']).reshape(-1, 1)
gamma = np.array(outcomes['gamma']).reshape(-1, 1)
# log values of gamma=0 are ignored
log_gamma = np.array([np.log10(value) for value in outcomes['gamma'] if value > 0]).reshape(-1, 1)
area_logG = area[:len(log_gamma)]
reg_gamma = LinearRegression().fit(log_gamma, area_logG)
area_g = reg_gamma.predict(log_gamma)
reg_beta = LinearRegression().fit(beta, area)
area_b = reg_beta.predict(beta)

fig, axs = plt.subplots(1,2)
fig.suptitle(r'Scatter plots of $\beta$ and $\gamma$ vs frozen area')
# plot  for beta
axs[0].plot(beta, area, '.')
axs[0].plot(beta, area_b, color = 'black')
axs[0].set_xlabel(r'$\beta$')
fig.text(0.35, 0.5, f'$r^2$ = {round(reg_beta.score(beta, area), 3)}')

# plot for gamma
axs[1].plot(gamma, area, '.', label = '')
axs[1].plot(gamma[len(gamma)-len(log_gamma):], area_g, color = 'black', label = 'prediction gamma')
axs[1].set_xscale('log')
axs[1].set_xlabel(r'$log(\gamma)$')
fig.text(0.04, 0.5, '% frozen area', va='center', rotation='vertical')
fig.text(0.7, 0.5, f'$r^2$ = {round(reg_gamma.score(log_gamma, area_logG), 3)}')
plt.show()
