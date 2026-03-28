package espol.spacehack.ecoshieldec.ui;

import android.os.Bundle;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import espol.spacehack.ecoshieldec.R;
import espol.spacehack.ecoshieldec.ui.fragments.ActivitiesFragment;
import espol.spacehack.ecoshieldec.ui.fragments.MapDashboardFragment;
import espol.spacehack.ecoshieldec.ui.fragments.RewardsFragment;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BottomNavigationView bottomNav = findViewById(R.id.bottom_navigation);

        bottomNav.setOnItemSelectedListener(item -> {
            int itemId = item.getItemId();

            if (itemId == R.id.nav_map) {
                loadFragment(new MapDashboardFragment());
                return true;

            } else if (itemId == R.id.nav_activities) {
                loadFragment(new ActivitiesFragment());
                return true;

            } else if (itemId == R.id.nav_rewards) {
                loadFragment(new RewardsFragment());
                return true;

            } else {
                Toast.makeText(this, "Sección en desarrollo", Toast.LENGTH_SHORT).show();
                return true;
            }
        });

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