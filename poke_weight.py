import requests
import pandas as pd

def get_all_pokemon_sv():
    # ポケモンのリストを取得
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)
    response.raise_for_status()
    all_pokemon = response.json()['results']
    
    # SV世代ポケモンのフィルタリング（例: 第9世代）
    sv_pokemon = []
    for pokemon in all_pokemon:
        pokemon_data = requests.get(pokemon['url']).json()
        # 第9世代を判別するフィールドをチェック
        if pokemon_data['game_indices']:
            games = [game['version']['name'] for game in pokemon_data['game_indices']]
            if 'scarlet' in games or 'violet' in games:
                sv_pokemon.append({
                    'name': pokemon_data['name'],
                    'types': [t['type']['name'] for t in pokemon_data['types']],
                    'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
                })

    return sv_pokemon

def save_to_csv(pokemon_data, filename):
    # データを整形してCSVに保存
    rows = []
    for pokemon in pokemon_data:
        row = {
            'name': pokemon['name'],
            'type_1': pokemon['types'][0] if len(pokemon['types']) > 0 else None,
            'type_2': pokemon['types'][1] if len(pokemon['types']) > 1 else None,
            'hp': pokemon['stats'].get('hp', None),
            'attack': pokemon['stats'].get('attack', None),
            'defense': pokemon['stats'].get('defense', None),
            'special-attack': pokemon['stats'].get('special-attack', None),
            'special-defense': pokemon['stats'].get('special-defense', None),
            'speed': pokemon['stats'].get('speed', None)
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"CSV saved to {filename}")

# 実行
if __name__ == "__main__":
    sv_pokemon = get_all_pokemon_sv()
    save_to_csv(sv_pokemon, "pokemon_sv_data.csv")
