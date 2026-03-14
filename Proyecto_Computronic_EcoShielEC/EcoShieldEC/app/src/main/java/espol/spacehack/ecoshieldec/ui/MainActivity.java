package espol.spacehack.ecoshieldec.ui;

import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import espol.spacehack.ecoshieldec.R;
import espol.spacehack.ecoshieldec.model.AlertResponse;
import espol.spacehack.ecoshieldec.network.ApiClient;
import espol.spacehack.ecoshieldec.network.ApiService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

// Importaciones del Mapa (Osmdroid)
import org.osmdroid.config.Configuration;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.api.IMapController;
import org.osmdroid.views.overlay.Marker;

public class MainActivity extends AppCompatActivity {

    // Declaramos las variables para controlar la pantalla
    private TextView tvSatelliteStatus;
    private TextView tvSensorStatus;
    private Button btnRefresh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // --- MAPA: Configuración obligatoria ANTES de dibujar la pantalla ---
        Configuration.getInstance().load(getApplicationContext(), getSharedPreferences("osmdroid", MODE_PRIVATE));

        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        // Ajuste de los bordes del celular (Edge-to-Edge)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Enlazamos las variables de Java con los IDs de nuestro diseño XML
        tvSatelliteStatus = findViewById(R.id.tv_satellite_status);
        tvSensorStatus = findViewById(R.id.tv_sensor_status);
        btnRefresh = findViewById(R.id.btn_refresh);

        // --- MAPA: Lógica para mostrar Guayaquil y el Marcador ---
        MapView map = findViewById(R.id.mapview);
        map.setMultiTouchControls(true); // Permite hacer zoom con los dedos
        IMapController mapController = map.getController();
        mapController.setZoom(13.0); // Nivel de zoom perfecto para ver el manglar y la ciudad

        // Coordenadas del Manglar en el Estero Salado (Guayaquil)
        GeoPoint sensorLocation = new GeoPoint(-2.203816, -79.897453);
        mapController.setCenter(sensorLocation);

        // Creamos el Pin/Marcador del Sensor IoT de Aarón
        Marker iotMarker = new Marker(map);
        iotMarker.setPosition(sensorLocation);
        iotMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_BOTTOM);
        iotMarker.setTitle("📡 Nodo IoT Activo (Sensor de Aarón)");
        iotMarker.setSnippet("Monitoreando nivel de agua en tiempo real");
        map.getOverlays().add(iotMarker); // Agregamos el pin al mapa

        // Le damos vida al botón
        btnRefresh.setOnClickListener(v -> {
            // Cambiamos el texto temporalmente para que el usuario sepa que está cargando
            tvSatelliteStatus.setText("📡 Satélite: Conectando con la nube...");
            tvSensorStatus.setText("🌊 Sensor IoT: Conectando con nodo local...");

            // Llamamos a nuestra función de internet
            obtenerDatosDelServidor();
        });
    }

    private void obtenerDatosDelServidor() {
        // Encendemos el motor de Retrofit
        ApiService service = ApiClient.getClient().create(ApiService.class);

        // Hacemos la llamada en segundo plano (para no congelar el celular)
        Call<AlertResponse> call = service.getMangroveStatus();
        call.enqueue(new Callback<AlertResponse>() {

            @Override
            public void onResponse(Call<AlertResponse> call, Response<AlertResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    // ¡ÉXITO! Adrián y Doménica nos mandaron la data real
                    AlertResponse alerta = response.body();

                    tvSatelliteStatus.setText("📡 Satélite (" + alerta.satelliteData.source + "): NDVI "
                            + alerta.satelliteData.mangroveHealthNdvi + " - " + alerta.satelliteData.status);

                    tvSensorStatus.setText("🌊 Sensor IoT (" + alerta.iotSensorData.sensorId + "): Nivel "
                            + alerta.iotSensorData.waterLevelCm + "cm - " + alerta.iotSensorData.status);

                    Toast.makeText(MainActivity.this, "Datos en tiempo real obtenidos", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<AlertResponse> call, Throwable t) {
                // FALLO: Como el servidor aún no existe, el código entrará por aquí.
                Log.e("SPACEHACK_API", "Error de servidor: " + t.getMessage());

                // Mostramos un mensajito en pantalla
                Toast.makeText(MainActivity.this, "Servidor apagado. Cargando simulación local...", Toast.LENGTH_LONG).show();

                // Mostramos datos simulados (Hardcoded) para poder hacer pruebas y tomar capturas
                tvSatelliteStatus.setText("📡 Satélite (Sentinel-2): NDVI 0.42 - ALERTA (Nubosidad 85%)");
                tvSensorStatus.setText("🌊 Sensor IoT (SH-NODE-01): Nivel 145.2cm - CRÍTICO 🚨");
            }
        });
    }
}