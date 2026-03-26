import ee


class ImageAnalysisService:
    @staticmethod
    def get_mean_value_at_point(image: ee.Image, point: ee.Geometry, scale: int = 10) -> ee.Dictionary:
        return image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=scale
        )