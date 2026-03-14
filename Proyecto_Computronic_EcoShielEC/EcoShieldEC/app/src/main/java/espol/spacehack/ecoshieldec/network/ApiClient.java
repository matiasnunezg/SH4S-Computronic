package espol.spacehack.ecoshieldec.network;

import espol.spacehack.ecoshieldec.utils.Constants;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    private static Retrofit retrofit = null;

    // Este método nos entrega el motor listo para usar en cualquier parte de la app
    public static Retrofit getClient() {
        if (retrofit == null) {
            retrofit = new Retrofit.Builder()
                    .baseUrl(Constants.BASE_URL_API) // La URL de tu archivo Constants
                    .addConverterFactory(GsonConverterFactory.create()) // Traduce el JSON a código Java automáticamente
                    .build();
        }
        return retrofit;
    }
}