import time
import requests

print("--- 1. Consulta GraphQL (Countries) ---")
consulta_paises = """
query {
  countries(filter: {code: {in: ["MX", "AR", "BR", "CO", "PE", "CL", "ES", "US", "CA", "JP"]}}) {
    name
    capital
    currency
  }
}
"""
t0 = time.perf_counter()
r_gql = requests.post("https://countries.trevorblades.com/", json={"query": consulta_paises}, timeout=10)
ms_gql = (time.perf_counter() - t0) * 1000
print(f"GraphQL Countries: {len(r_gql.content)} bytes | {ms_gql:.1f} ms")


print("\n--- 2. Comparación PokéAPI: REST vs GraphQL ---")
pokemons = ["pikachu", "bulbasaur", "charmander", "squirtle", "eevee", "snorlax", "gengar", "onix", "psyduck", "jigglypuff"]

# REST: 10 peticiones
bytes_rest = 0
t0 = time.perf_counter()
for p in pokemons:
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{p}", timeout=10)
    bytes_rest += len(r.content)
ms_rest = (time.perf_counter() - t0) * 1000

print(f"REST (10 peticiones): {bytes_rest} bytes | {ms_rest:.1f} ms")

# GraphQL: 1 sola petición
consulta_poke = """
query {
  pokemon_v2_pokemon(where: {name: {_in: ["pikachu", "bulbasaur", "charmander", "squirtle", "eevee", "snorlax", "gengar", "onix", "psyduck", "jigglypuff"]}}) {
    name
    height
    pokemon_v2_pokemontypes {
      pokemon_v2_type { name }
    }
  }
}
"""
t0 = time.perf_counter()
r_poke_gql = requests.post("https://beta.pokeapi.co/graphql/v1beta", json={"query": consulta_poke}, timeout=10)
ms_poke_gql = (time.perf_counter() - t0) * 1000
bytes_poke_gql = len(r_poke_gql.content)

print(f"GraphQL (1 petición): {bytes_poke_gql} bytes | {ms_poke_gql:.1f} ms")