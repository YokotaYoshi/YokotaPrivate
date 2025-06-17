import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List

# --- Google Sheetsの読み込み ---
def load_sheet_data(sheet_url: str) -> List[dict]:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_values()[1:]  # ヘッダーをスキップ

    players = []
    for row in data:
        if len(row) < 4:
            continue
        name = row[0]
        try:
            power = int(row[1])
            priority = int(row[2])
            position = int(row[3])
        except ValueError:
            continue

        players.append({
            "name": name,
            "power": power,
            "priority": priority,  # 0:必須, 1:優先, 2:調整
            "position": position   # 0:前中衛, 1:後衛
        })
    return players

# --- チーム編成アルゴリズム（簡略構成でスケルトン） ---
def assign_teams(players: List[dict], team_count: int = 4):
    teams = [[] for _ in range(team_count)]
    xp = [0 for _ in range(team_count)]

    # 優先度ごとに分ける
    must = [p for p in players if p["priority"] == 0]
    priority = [p for p in players if p["priority"] == 1]
    flexible = [p for p in players if p["priority"] == 2]

    # STEP 1: 必須枠 前・中衛を先に割り当て
    must_front = sorted([p for p in must if p["position"] == 0], key=lambda x: -x["power"])
    must_back = sorted([p for p in must if p["position"] == 1], key=lambda x: x["power"])  # 後衛は低パワーから

    i = 0
    for p in must_front:
        teams[i % team_count].append(p)
        xp[i % team_count] += p["power"]
        i += 1

    for j in range(team_count - len(must_front)):
        if j < len(must_back):
            idx = (i + j) % team_count
            teams[idx].append(must_back[j])
            xp[idx] += must_back[j]["power"]

    # STEP 2: 優先枠 後衛をできるだけ均等に入れる
    priority_back = sorted([p for p in priority if p["position"] == 1], key=lambda x: x["power"])
    used = set()
    for i in range(team_count):
        for p in priority_back:
            if p["name"] not in used and not any(mem["position"] == 1 for mem in teams[i]):
                teams[i].append(p)
                xp[i] += p["power"]
                used.add(p["name"])
                break

    # STEP 3: 優先枠 残りをパワー順に入れる
    for p in sorted(priority, key=lambda x: -x["power"]):
        if p["name"] in used:
            continue
        for i in sorted(range(team_count), key=lambda x: xp[x]):
            if xp[i] + p["power"] <= 10600:
                teams[i].append(p)
                xp[i] += p["power"]
                used.add(p["name"])
                break

    # STEP 4: 調整枠を順次追加（バランス取り）
    for p in sorted(flexible, key=lambda x: -x["power"]):
        for i in sorted(range(team_count), key=lambda x: xp[x]):
            if xp[i] + p["power"] <= 10600:
                teams[i].append(p)
                xp[i] += p["power"]
                break

    return teams, xp

# --- 結果出力 ---
def print_teams(teams, xp):
    for i, team in enumerate(teams):
        print(f"\nTeam {i+1} (XP: {xp[i]}, Avg: {xp[i]/len(team):.2f})")
        for p in team:
            pos = "前中衛" if p["position"] == 0 else "後衛"
            kind = ["必須", "優先", "調整"][p["priority"]]
            print(f"  {p['name']} - {p['power']}pt ({kind}, {pos})")

# --- 実行部 ---
if __name__ == "__main__":
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1X4FtjJWwblWUuj4Ngg9divxUsqsJFQt9Soa-osF9EXg/edit#gid=0"
    players = load_sheet_data(SHEET_URL)
    teams, xp = assign_teams(players, team_count=4)
    print_teams(teams, xp)
