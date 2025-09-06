import api from "./api";

type Option = "animations" | "base";

export const GetPokemonFiles = async (pokemon_id: number, option: Option) => {
  try {
    const response = await api.get("/pokemon/get_all_pokemon_images/", {
      params: {
        pokemon_id: pokemon_id,
        option: option,
      },
    });
    return response.data;
  } catch (error) {
    console.log(error);
  }
};
