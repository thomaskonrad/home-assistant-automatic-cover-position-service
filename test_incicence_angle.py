import unittest
from incidence_angle import get_incidence_angle


class TestIncidenceAngles(unittest.TestCase):
    def test_regular_window_full_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=90,  # east
                sun_elevation_degrees=0,  # horizon
                window_normal_azimuth_degrees=90,  # east
                window_normal_elevation_degrees=0,  # regular window
            ),
            90,
        )

    def test_skylight_window_45_degrees_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=270,  # west
                sun_elevation_degrees=0,  # horizon
                window_normal_azimuth_degrees=270,  # west
                window_normal_elevation_degrees=45,  # skylight window
            ),
            45,
        )

    def test_regular_window_45_degrees_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=90,  # east
                sun_elevation_degrees=0,  # horizon
                window_normal_azimuth_degrees=135,  # southeast
                window_normal_elevation_degrees=0,  # regular window
            ),
            45,
        )

    def test_regular_window_0_degrees_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=180,  # south
                sun_elevation_degrees=45,  # elevated
                window_normal_azimuth_degrees=270,  # west
                window_normal_elevation_degrees=0,  # regular window
            ),
            0,
        )

    def test_skylight_window_30_degrees_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=180,  # south
                sun_elevation_degrees=45,  # elevated
                window_normal_azimuth_degrees=270,  # west
                window_normal_elevation_degrees=45,  # skylight window
            ),
            30,
        )

    def test_skylight_window_negative_solar_radiation(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=135,  # southeast
                sun_elevation_degrees=45,  # elevated
                window_normal_azimuth_degrees=270,  # west
                window_normal_elevation_degrees=0,  # regular window
            ),
            0,
        )

    def test_skylight_window_sun_below_horizon(self):
        self.assertEqual(
            get_incidence_angle(
                sun_azimuth_degrees=45,  # northeast
                sun_elevation_degrees=-45,  # below horizon
                window_normal_azimuth_degrees=45,  # northeast
                window_normal_elevation_degrees=45,  # skylight window
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
