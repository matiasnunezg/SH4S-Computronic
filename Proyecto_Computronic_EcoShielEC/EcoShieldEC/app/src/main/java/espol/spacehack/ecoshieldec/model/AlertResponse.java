package espol.spacehack.ecoshieldec.model;

public class AlertResponse {
    public String alertId;
    public String timestamp;
    public LocationData location;
    public SatelliteData satelliteData;
    public IoTSensorData iotSensorData;
    public AnalysisData analysis;

    public static class LocationData {
        public String zone;
        public double lat;
        public double lng;
    }

    public static class SatelliteData {
        public String source;
        public double cloudCoverPercentage;
        public double mangroveHealthNdvi;
        public String status;
    }

    public static class IoTSensorData {
        public String sensorId;
        public double waterLevelCm;
        public boolean isOnline;
        public String status;
    }

    public static class AnalysisData {
        public String overallRiskLevel;
        public int riskScore;
        public String message;
        public String recommendedAction;
    }
}