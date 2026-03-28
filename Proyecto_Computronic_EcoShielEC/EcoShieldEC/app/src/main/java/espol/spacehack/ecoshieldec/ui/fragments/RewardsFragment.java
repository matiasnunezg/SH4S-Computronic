package espol.spacehack.ecoshieldec.ui.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import espol.spacehack.ecoshieldec.R;

public class RewardsFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        // Inflamos el XML de Doménica (ya limpio sin el menú)
        return inflater.inflate(R.layout.fragment_rewards, container, false);
    }

    // Aquí Doménica agregará la lógica de sus RecyclerViews más adelante
}