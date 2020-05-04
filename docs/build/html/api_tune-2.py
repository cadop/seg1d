# Now another noisy sine wave is created and a segment of it is cut out.

# define a segment within the sine wave to use as reference
t_s,t_e = 200,400
# number of reference datasets to generate for the example

# make reference data with different random noise on a segment of the original
np.random.seed(123)
refData = segnoise.add_noise(np.sin(x),snr=45)[t_s:t_e] 

# The reference data looks like:

plt.figure(figsize=(3,3)) #doctest: +SKIP
# Plot the reference
plt.plot(x[t_s:t_e], refData,linewidth=4,alpha=0.5,label='Reference')#doctest: +SKIP
plt.xlabel('Angle [rad]')#doctest: +SKIP
plt.ylabel('sin(x)')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.tight_layout()#doctest: +SKIP
plt.show()#doctest: +SKIP
