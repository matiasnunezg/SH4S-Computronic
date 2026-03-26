import ee

class NDVIService:
    def generate_layer(image: ee.Image) -> ee.Image:
        return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    def get_ndvi_value_at_point(ndvi_image: ee.Image, point: ee.Geometry, scale: int = 10) -> float | None:
        result = ndvi_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=scale
        ).getInfo()

        return result.get("NDVI") if result else None