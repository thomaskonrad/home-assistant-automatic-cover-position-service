import sys
import math


def get_incidence_angle(
    sun_azimuth_degrees: float,
    sun_elevation_degrees: float,
    window_normal_azimuth_degrees: float,
    window_normal_elevation_degrees: float,
):
    sun_azimuth_radians = math.radians(sun_azimuth_degrees)
    sun_inclination_radians = math.radians(90.0 - sun_elevation_degrees)
    window_azimuth_radians = math.radians(window_normal_azimuth_degrees)
    window_inclination_radians = math.radians(90.0 - window_normal_elevation_degrees)

    angle_radians = math.acos(
        math.cos(sun_inclination_radians) * math.cos(window_inclination_radians)
        + (
            math.sin(sun_inclination_radians)
            * math.sin(window_inclination_radians)
            * math.cos(window_azimuth_radians - sun_azimuth_radians)
        )
    )

    angle = round(90 - math.degrees(angle_radians), 1)

    if angle < 0:
        return 0
    else:
        return angle
