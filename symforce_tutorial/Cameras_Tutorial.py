import symforce.symbolic as sf
from symforce.notebook_util import display

# Let’s start by creating a linear camera calibration object:
linear_camera_cal = sf.LinearCameraCal.symbolic("cal")
display(linear_camera_cal)

# This lets us project/deproject points written in the camera frame as so:
camera_pixel = sf.V2.symbolic("p")

"""
单个下划线是一个"don't care"变量名，通常用于忽略不需要的返回值，例如在使用_接收print函数的返回值。
_ = print("Hello, World!")


camera_ray_from_pixel(pixel, epsilon=0.0, normalize=False)函数的返回类型是一个元组
RETURN TYPE:
Tuple[Matrix31, float]
"""
# 从2d像素坐标反投影到Camera frame的3d归一化坐标
camera_ray, _ = linear_camera_cal.camera_ray_from_pixel(camera_pixel)
# camera_ray, is_valid = linear_camera_cal.camera_ray_from_pixel(camera_pixel)
display(camera_ray)
# display(is_valid)


camera_point_reprojected, _ = linear_camera_cal.pixel_from_camera_point(
    camera_ray,
)
display(camera_point_reprojected)



# Using camera calibration objects, we can create cameras with additional parameters, such as an image size:
linear_camera = sf.Camera(
    calibration=sf.LinearCameraCal(
        focal_length=(440, 400),
        principal_point=(320, 240),
    ),
    image_size=(640, 480),
)
display(linear_camera)



"""
Now, when projecting points into the image frame, we can check whether the resulting point is in the bounds determined by image_size:
"""
point_in_FOV = sf.V3(0, 0, 1)
point_outside_FOV = sf.V3(100, 0, 1)
for point in (point_in_FOV, point_outside_FOV):
    pixel, is_valid = linear_camera.pixel_from_camera_point(point)
    print(
        "point={} -> pixel={}, is_valid={}".format(
            point.to_storage(),
            pixel.to_storage(),
            is_valid,
        )
    )



# We can also create a camera with a given pose:
linear_posed_camera = sf.PosedCamera(
    pose=sf.Pose3(
        # camera is spun 180 degrees about y-axis
        R=sf.Rot3.from_yaw_pitch_roll(0, sf.pi, 0),
        t=sf.V3(),
    ),
    calibration=linear_camera.calibration,
    image_size=(640, 480),
)
display(linear_posed_camera)


# The given pose can be used to transform points between a global frame and the image frame:

global_point = sf.V3(0, 0, -1)
print(
    "point in global coordinates={} (in camera coordinates={})".format(
        global_point.to_storage(),
        (linear_posed_camera.pose * global_point).to_storage(),
    )
)

"""
pixel_from_global_point函数说明：
Transforms the given point into the camera frame using the given camera pose, and then uses the given camera calibration to compute the resulted pixel coordinates of the projected point.
"""
pixel, is_valid = linear_posed_camera.pixel_from_global_point(global_point)
print(
    "global_point={} -> pixel={}, is_valid={}".format(
        global_point.to_storage(), pixel.to_storage(), is_valid
    )
)


# We can also transform points in pixel coordinates back into the global frame (given a range):
range_to_point = (global_point - linear_posed_camera.pose.t).norm()
global_point_reprojected, is_valid = linear_posed_camera.global_point_from_pixel(
    pixel, range_to_point=range_to_point
)
display(global_point_reprojected)



"""
Finally, we can warp points between two posed cameras given the location of the pixel in the source camera, the inverse range to the point, and the target camera to warp the point into.
"""

"""
最后，我们可以在两个posed cameras之间变换点，给定源相机中像素的位置，沿着射线到全局点的逆距离(其实应该就是逆深度)，和变换点进去的目标相机。

warp_pixel投影一个像素点从一个相机到另一个相机
"""

# Perturb second camera slightly from first (small angular change in roll)
perturbed_rotation = linear_posed_camera.pose.R * sf.Rot3.from_yaw_pitch_roll(0, 0, 0.5)
target_posed_cam = sf.PosedCamera(
    pose=sf.Pose3(R=perturbed_rotation, t=sf.V3()),
    calibration=linear_camera.calibration,
)
# Warp pixel from source camera into target camera given inverse range
target_pixel, is_valid = linear_posed_camera.warp_pixel(
    pixel=sf.V2(320, 240),
    #inverse_range=1.0,
    inverse_range=2.0, # 不管逆深度是多少，最后像素坐标都是同一个
    target_cam=target_posed_cam,
)
display(target_pixel)



"""
In the examples above we used a linear calibration, but we can use other types of calibrations as well:
其它相机模型也可以工作的很好
"""

atan_cam = sf.ATANCameraCal(
    focal_length=[380.0, 380.0],
    principal_point=[320.0, 240.0],
    omega=0.35,
)
# 将像素坐标转换为归一化坐标
camera_ray, is_valid = atan_cam.camera_ray_from_pixel(sf.V2(50.0, 50.0))
display(camera_ray)
# 将归一化坐标转换为像素坐标
pixel, is_valid = atan_cam.pixel_from_camera_point(camera_ray)
display(pixel)

