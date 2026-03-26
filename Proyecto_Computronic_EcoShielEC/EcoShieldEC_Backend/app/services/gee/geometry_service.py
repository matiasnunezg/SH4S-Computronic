import ee

class GeometryService:
    @staticmethod
    def create_buffered_point(longitude: float, latitude: float, buffer_meters: float) -> ee.Geometry:
        return ee.Geometry.Point([longitude, latitude]).buffer(buffer_meters)

    @staticmethod
    def create_point(longitude: float, latitude: float) -> ee.Geometry:
        return ee.Geometry.Point([longitude, latitude])