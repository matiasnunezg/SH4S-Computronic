package espol.spacehack.ecoshieldec.ui.fragments;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import espol.spacehack.ecoshieldec.R;

// Importaciones del Mapa
import org.osmdroid.config.Configuration;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.api.IMapController;
import org.osmdroid.views.overlay.Marker;

import java.util.ArrayList;
import java.util.List;

public class MapDashboardFragment extends Fragment {

    private MapView map;
    private IMapController mapController;
    private List<GeoPoint> mangrovePoints;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        // Configuración obligatoria del mapa
        Context ctx = requireActivity().getApplicationContext();
        Configuration.getInstance().load(ctx, requireActivity().getSharedPreferences("osmdroid", Context.MODE_PRIVATE));

        return inflater.inflate(R.layout.fragment_map_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // Enlazamos SOLO el mapa (ya no hay botones)
        map = view.findViewById(R.id.mapview);

        map.setMultiTouchControls(true);
        mapController = map.getController();
        mapController.setZoom(12.0); // Zoom perfecto para Guayaquil

        // Centro: Golfo de Guayaquil
        GeoPoint sensorLocation = new GeoPoint(-2.503816, -79.897453);
        mapController.setCenter(sensorLocation);

        // Cargamos los múltiples puntos
        loadMockMangroveData();

        for (GeoPoint point : mangrovePoints) {
            Marker marker = new Marker(map);
            marker.setPosition(point);
            marker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM);

            if (point.getLatitude() == sensorLocation.getLatitude() && point.getLongitude() == sensorLocation.getLongitude()) {
                marker.setTitle("Gulf of Guayaquil (Primary Ecosystem)");
                marker.setSnippet("Core Hybrid Monitoring Area: Active");
            } else {
                marker.setTitle("Mangrove Protection Zone");
                marker.setSnippet("Ecosystem Status: Active (Satellite Sync)");
            }
            map.getOverlays().add(marker);
        }
    }

    private void loadMockMangroveData() {
        mangrovePoints = new ArrayList<>();
        mangrovePoints.add(new GeoPoint(-2.503816, -79.897453)); // Golfo
        mangrovePoints.add(new GeoPoint(-2.217303, -79.888568)); // Santay
        mangrovePoints.add(new GeoPoint(-2.179374, -79.916823)); // Estero Norte
        mangrovePoints.add(new GeoPoint(-2.177093, -79.851963)); // Duran
        mangrovePoints.add(new GeoPoint(-2.247271, -79.854194)); // Rio Babahoyo
    }

    @Override
    public void onResume() { super.onResume(); if (map != null) map.onResume(); }

    @Override
    public void onPause() { super.onPause(); if (map != null) map.onPause(); }
}