import ee

class DEMService:
    def get_elevation_value_at_point(dem_image: ee.Image, point: ee.Geometry, scale: int = 30) -> float | None:
        result = dem_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=scale
        ).getInfo()

        return result.get("elevation") if result else None