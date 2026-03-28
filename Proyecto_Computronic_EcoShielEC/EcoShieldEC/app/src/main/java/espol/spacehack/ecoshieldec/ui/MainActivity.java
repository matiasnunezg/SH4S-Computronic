package espol.spacehack.ecoshieldec.ui;

import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import espol.spacehack.ecoshieldec.R;
import espol.spacehack.ecoshieldec.ui.fragments.*;



public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Carga el cascarón con el menú inferior

        BottomNavigationView bottomNav = findViewById(R.id.bottom_navigation);

        bottomNav.setOnItemSelectedListener(item -> {
            int itemId = item.getItemId();

            if (itemId == R.id.nav_map) {
                // Carga la SECCIÓN 1 (Matías)
                loadFragment(new MapDashboardFragment());
                return true;
            } else if (itemId == R.id.nav_rewards) {
                // Carga la SECCIÓN 5 (Doménica)
                loadFragment(new RewardsFragment());
                return true;
            } else {
                // Para las demás, mostramos un mensaje temporal
                Toast.makeText(this, "Sección en desarrollo", Toast.LENGTH_SHORT).show();
                return true;
            }
        });

        // Al abrir la app, cargamos TU MAPA por defecto
        if (savedInstanceState == null) {
            bottomNav.setSelectedItemId(R.id.nav_map);
        }
    }

    private void loadFragment(Fragment fragment) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.fragment_container, fragment)
                .commit();
    }
}