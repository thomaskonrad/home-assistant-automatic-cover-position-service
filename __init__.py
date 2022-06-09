from .incidence_angle import get_incidence_angle
import math

DOMAIN = "automatic_cover_position_service"

ATTR_TARGET_SOLAR_IRRADIATION_PERCENT = "target_solar_irradiation_percent"
DEFAULT_TARGET_SOLAR_IRRADIATION_PERCENT = 10
ATTR_MINIMUM_SUN_ELEVATION = "minimum_sun_elevation"
DEFAULT_MINIMUM_SUN_ELEVATION = 10


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_set_automatic_cover_position(call):
        """Handle the service call."""
        target_solar_irradiation = (
            float(
                call.data.get(
                    ATTR_TARGET_SOLAR_IRRADIATION_PERCENT,
                    DEFAULT_TARGET_SOLAR_IRRADIATION_PERCENT,
                )
            )
            / 100
        )

        minimum_sun_elevation = int(
            call.data.get(
                ATTR_MINIMUM_SUN_ELEVATION,
                DEFAULT_MINIMUM_SUN_ELEVATION,
            )
        )

        sun_state = hass.states.get("sun.sun")
        sun_azimuth_degrees = sun_state.attributes.get("azimuth")
        sun_elevation_degrees = sun_state.attributes.get("elevation")

        for entity_id in call.data.get("entity_id"):
            if sun_elevation_degrees > minimum_sun_elevation:
                cover_state = hass.states.get(entity_id)

                window_azimuth_degrees = cover_state.attributes.get("azimuth")
                window_elevation_degrees = cover_state.attributes.get("elevation")
                window_open_offset = cover_state.attributes.get("open_position", 100)
                window_closed_offset = cover_state.attributes.get("closed_position", 12)

                incidence_angle = get_incidence_angle(
                    sun_azimuth_degrees=sun_azimuth_degrees,
                    sun_elevation_degrees=sun_elevation_degrees,
                    window_normal_azimuth_degrees=window_azimuth_degrees,
                    window_normal_elevation_degrees=window_elevation_degrees,
                )

                solar_irradiation = math.sin(math.radians(incidence_angle))

                if solar_irradiation > 0:
                    target_opening = target_solar_irradiation / solar_irradiation
                else:
                    target_opening = 1

                target_opening = min(target_opening, 1)

                opening_range = window_open_offset - window_closed_offset
                opening_factor = opening_range * target_opening

                target_position = round(window_closed_offset + opening_factor, 0)
            else:
                target_position = 100

            hass.services.call(
                "cover",
                "set_cover_position",
                {"position": target_position, "entity_id": entity_id},
            )

    hass.services.register(
        DOMAIN, "set_automatic_cover_position", handle_set_automatic_cover_position
    )

    # Return boolean to indicate that initialization was successful.
    return True
