# escapement wheel angle calculation
'''
init_val = 5
step = 0
for i in range(0,5):
    step += 10
    init_val += 5.5
    print(step, init_val)
    step += 10
    if i == 3:
        init_val += 1
    init_val += 20
    print(step, init_val)

print("estimated total deg", (init_val-5)/5*14)

'''
import math

# index 0, my clock index 1, example_clock, index 2, experimental (if applicable)
# point mass analysis

g = 980
L_com = [1.928*2.54, 5.7]

# area, thickness, density -> acrylic mass
A = [9.156*(2.54**2), 13.902*(2.54**2)]
t = [0.25*2.54, 0.21*2.54]
rho = 1.2


m = [A[i]*t[i]*rho for i in range(2)]
# mass per bolt (mistake of example clock?)
m_bolt = [2.75, 4]
m_total = [m[i] + m_bolt[i]*8 for i in range(2)]




L_bolt = [(8.89, 9.448, 10.795, 12.142, 12.7, 12.142, 10.795, 9.448),
          (9, 9.5, 10.8, 12, 12.6, 12, 10.8, 9.5)]
L_com_total = [(m[i]*L_com[i] + m_bolt[i]*sum(L_bolt[i]))/m_total[i] for i in range(2)]

# natural frequency
omega_pm = [(g/L_com_total[i])**(1/2) for i in range(2)]


# rigid body analysis (using rotational inertia), Izz of acrylic only
# TODO -> what is r_bolt for example clock?
Izz = [2136.821, 1661]
r_bolt = [(8.89, 9.544, 10.962, 12.217, 12.7, 12.217, 10.962, 9.544),
          (9, 9.5, 10.8, 12, 12.6, 12, 10.8, 9.5)]

I_bolt = [m_bolt[i]*sum([r**2 for r in r_bolt[i]]) for i in range(2)]
I_total = [Izz[i] + I_bolt[i] for i in range(2)]

# natural frequency, period
omega_rb = [(m_total[i]*g*L_com_total[i]/I_total[i])**(1/2) for i in range(2)]


# append experimental value
m.append(52)
m_total.append(78)
L_com.append(6)
L_com_total.append(7)
omega_pm.append(2*math.pi/(8/14))
omega_rb.append(2*math.pi/(8/14))

print("area", A)
print("thickness", t)
print("density", rho)
print("acrylic mass", m)
print("total mass", m_total)
print("acrylic center of mass", L_com)
print("total center of mass", L_com_total)
print("acrylic inertia", Izz)
print("bolt inertia", I_bolt)
print("total inertia", I_total)
print("natural frequency pm", omega_pm)
print("natural frequency rb", omega_rb)
print("period pm", [2*math.pi/val for val in omega_pm])
print("period rb", [2*math.pi/val for val in omega_rb])

def err(th_val, exp_val):
    return (th_val-exp_val)/exp_val
print("mass err", err(m_total[1], m_total[2]))
print("L_com err", err(L_com_total[1], L_com_total[2]))

period_pm = [2*math.pi/val for val in omega_pm]
period_rb = [2*math.pi/val for val in omega_rb]
print("freq err pm", err(omega_pm[1], omega_pm[2]))
print("freq err rb", err(omega_rb[1], omega_rb[2]))
print("period err pm", err(period_pm[1], period_pm[2]))
print("period err rb", err(period_rb[1], period_rb[2]))