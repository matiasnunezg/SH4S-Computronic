import ee


class CollectionService:
    def __init__(self, collection_id: str):
        self.collection_id = collection_id

    def get_collection(self, region: ee.Geometry, start_date: str, end_date: str, cloud_percentage: float = 20) -> ee.ImageCollection:
        return (
            ee.ImageCollection(self.collection_id)
            .filterBounds(region)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_percentage))
        )

    @staticmethod
    def get_median_image(collection: ee.ImageCollection) -> ee.Image:
        return collection.median()