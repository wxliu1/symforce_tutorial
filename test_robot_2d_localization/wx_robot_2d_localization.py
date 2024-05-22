import symforce
#symforce.set_epsilon_to_symbol()

import numpy as np
from symforce import typing as T
from symforce.values import Values
import symforce.symbolic as sf

'''
num_poses = 3
num_landmarks = 3

initial_values = Values(
    poses=[sf.Pose2.identity()] * num_poses,
    landmarks=[sf.V2(-2, 2), sf.V2(1, -3), sf.V2(5, 2)],
    distances=[1.7, 1.4],
    angles=np.deg2rad([[145, 335, 55], [185, 310, 70], [215, 310, 70]]).tolist(),
    epsilon=sf.numeric_epsilon,
)
'''

pose = sf.Pose2(
    t=sf.V2.symbolic("t"),
    R=sf.Rot2.symbolic("R")
)
landmark = sf.V2.symbolic("L")

landmark_body = pose.inverse() * landmark
'''
#print(sf.atan2(landmark[1], landmark[0]))
print(pose.R)
print(pose.t)

Rotate=sf.Rot2.symbolic("R")
print(Rotate)

print(landmark_body)
'''
#aaa=landmark_body.jacobian(pose)
#print(aaa)
bbb = sf.atan2(landmark_body[1], landmark_body[0])
print(bbb)

# print <Pose2 R=<Rot2 <C real=1, imag=0>>, t=(0, 0)>
print(sf.Pose2.identity())

# 2.220446049250313e-15
print(sf.numeric_epsilon)


'''
def build_initial_values() -> T.Tuple[Values, int, int]:
    """
    Creates a Values with numerical values for the constants in the problem, and initial guesses
    for the optimized variables
    """
    num_poses = 3
    num_landmarks = 3

    initial_values = Values(
        poses=[sf.Pose2.identity()] * num_poses,
        landmarks=[sf.V2(-2, 2), sf.V2(1, -3), sf.V2(5, 2)],
        distances=[1.7, 1.4],
        angles=np.deg2rad([[55, 245, -35], [95, 220, -20], [125, 220, -20]]).tolist(),
        epsilon=sf.numeric_epsilon,
    )

    return initial_values, num_poses, num_landmarks
'''

