import ee

class NDWIService:
    def generate_layer(image: ee.Image) -> ee.Image:
        return image.normalizedDifference(['B3', 'B8']).rename('NDWI')

    def get_ndwi_value_at_point(ndwi_image: ee.Image, point: ee.Geometry, scale: int = 10) -> float | None:
        result = ndwi_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=scale
        ).getInfo()

        return result.get("NDWI") if result else None