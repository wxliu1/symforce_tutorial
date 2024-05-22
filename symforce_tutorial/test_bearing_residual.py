import symforce
symforce.set_epsilon_to_symbol()

import symforce.symbolic as sf
from symforce.notebook_util import display
from symforce.notebook_util import print_expression_tree



def bearing_residual(
    pose: sf.Pose2, landmark: sf.V2, angle: sf.Scalar, epsilon: sf.Scalar
) -> sf.V1:
    """
    Residual from a relative bearing measurement of a 2D pose to a landmark.
    """
    # 一个路标点的2D位姿的相对方位测量的残差

    # 把路标点从world系转到body系
    t_body = pose.inverse() * landmark
    # 根据路标点的2D坐标计算相对方位角度(relative bearing angle):反正切计算公式atan2(y, x)
    predicted_angle = sf.atan2(t_body[1], t_body[0], epsilon=epsilon)
    # 预测值减去测量值
    return sf.V1(sf.wrap_angle(predicted_angle - angle))
    

 
pose = sf.Pose2(
    t=sf.V2.symbolic("t"),
    R=sf.Rot2.symbolic("R")
)
landmark = sf.V2.symbolic("L")
angle = sf.Symbol("a")
epsilon=sf.epsilon()
 
#display(landmark_body)

norm=sf.V3.symbolic("x").norm(epsilon=sf.epsilon())
#display(norm)
#display(sf.epsilon())

retval=bearing_residual(pose, landmark, angle, epsilon)
display(retval)
