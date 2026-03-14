package espol.spacehack.ecoshieldec.network;

import espol.spacehack.ecoshieldec.model.AlertResponse;
import retrofit2.Call;
import retrofit2.http.GET;

public interface ApiService {

    // Aquí definimos la ruta (endpoint) a la que la app va a "tocar la puerta".
    // Doménica te dará la ruta final, por ahora dejamos esta de prueba.
    @GET("api/v1/manglares/status")
    Call<AlertResponse> getMangroveStatus();

}