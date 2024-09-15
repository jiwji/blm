import requests
import random
import time

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info
from core.token import get_token


def play_game(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/game/play"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        game_id = data["gameId"]
        return game_id
    except:
        return None


def claim_game(token, game_id, point, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    payload = {"gameId": game_id, "points": point}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.text
        return data
    except:
        return None


def process_play_game(data, proxies=None):
    while True:
        token = get_token(data=data, proxies=proxies)
        ticket = get_info(token=token, proxies=proxies)
        if ticket is None:
            base.log(f"{base.white}Auto Play Game: {base.red}Ticket data not found")
            break

        if ticket > 0:
            base.log(f"{base.green}Available tickets: {base.white}{ticket}")
            game_id = play_game(token=token, proxies=proxies)
            if game_id:
                play_time = random.uniform(27, 30)
                base.log(f"{base.yellow}Playing for {play_time:.2f} seconds...")
                time.sleep(play_time)
                point = random.randint(160, 250)
                
                max_retries = 5
                for attempt in range(max_retries):
                    claim = claim_game(
                        token=token, game_id=game_id, point=point, proxies=proxies
                    )
                    if claim == "OK":
                        base.log(
                            f"{base.white}Auto Play Game: {base.green}Success | Added {point} points"
                        )
                        break
                    else:
                        if attempt < max_retries - 1:
                            base.log(f"{base.white}Auto Play Game: {base.yellow}Claim Point Fail. Retrying in 1 seconds... (Attempt {attempt + 1}/{max_retries})")
                            time.sleep(1)
                        else:
                            base.log(f"{base.white}Auto Play Game: {base.red}Claim Point Fail after {max_retries} attempts")
                            return  # Exit the function after max retries
            else:
                base.log(f"{base.white}Auto Play Game: {base.red}Game ID not Found")
                break
        else:
            base.log(f"{base.white}Auto Play Game: {base.red}No ticket available")
            break
