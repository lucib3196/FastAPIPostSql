import api from "./api";

type Option = "animations" | "base";

export const GetPokemonFiles = async (pokemon_id: number, option: Option) => {
  try {
    const response = await api.get(`/pf/${pokemon_id}/images/${option}`, {
      params: {
        pokemon_id: pokemon_id,
        option: option,
      },
    });
    console.log("This is the response", response)
    return response.data;
  } catch (error) {
    console.log("This is the response", error)
    console.log(error);
  }
};
