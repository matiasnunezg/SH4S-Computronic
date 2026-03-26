import ee


class IndexService:
    @staticmethod
    def calculate_ndvi(image: ee.Image) -> ee.Image:
        return image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    @staticmethod
    def calculate_threshold_mask(image: ee.Image, threshold: float, name: str = "Mask") -> ee.Image:
        return image.gt(threshold).selfMask().rename(name)