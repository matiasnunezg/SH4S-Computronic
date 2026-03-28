package espol.spacehack.ecoshieldec.ui.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.material.card.MaterialCardView;

import espol.spacehack.ecoshieldec.R;

public class MangroveInfoFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_mangrove_info, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        MaterialCardView cardAlerts = view.findViewById(R.id.cardAlertHistory);
        MaterialCardView cardWater = view.findViewById(R.id.cardWaterQuality);
        MaterialCardView cardReports = view.findViewById(R.id.cardActivityReports);

        cardAlerts.setOnClickListener(v -> Toast.makeText(requireContext(), "Opening Environmental Event Log", Toast.LENGTH_SHORT).show());
        cardWater.setOnClickListener(v -> Toast.makeText(requireContext(), "Fetching Historical IoT Parameters", Toast.LENGTH_SHORT).show());
        cardReports.setOnClickListener(v -> Toast.makeText(requireContext(), "Loading Community Conservation activities", Toast.LENGTH_SHORT).show());

    }
}