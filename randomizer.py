import json
import random
import qrcode
from PIL import Image, ImageDraw, ImageFont


def read_params(filename='params.json'):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def read_gg(gg_num):
    with open(f'gg{gg_num}.json', 'r') as file:
        data = json.load(file)
    return data

def randomize_round(gg, round_num):
    selected_strategy = gg['strategies'].pop()
    selected_deployment = gg['deployments'].pop()
    selected_schemes = random.sample(gg['schemes'], 5)

    pool = {
        "Name": "Round " + str((round_num+1)),
        "Strategy": selected_strategy,
        "Deployment": selected_deployment,
        "Schemes": selected_schemes
    }
    
    return pool

def generate_qr(round, app_ver, max_crew_size, index):
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)

    data_input = {
        "specialRules": {"Singles": {"name": "Singles", "value": None}},
        "name": round["Name"],
        "ruleset": "GG Season 4",
        "strat": round["Strategy"],
        "deployment": round["Deployment"],
        "maxCrewSize": max_crew_size,
        "createdIn": app_ver,
        "created": "2024-08-21T21:37:00.000",
        "schemePool": round["Schemes"]
    }
    qr_img = qrcode.make(json.dumps(data_input))

    img0 = Image.new('RGB', (795, 1520), color='white')
    
    img0.paste(qr_img, (0, 730))

    draw = ImageDraw.Draw(img0)
    draw.text((40, 40), round["Name"], fill='black', font=font)
    draw.text((50, 120), round["Strategy"], fill='black', font=font)
    draw.text((50, 180), round["Deployment"], fill='black', font=font)

    for i, scheme in enumerate(round["Schemes"]):
        y = 300 + i * 60
        draw.text((50, y), scheme, fill='black', font=font)

    img_name = f"img{1 + index}.png"
    img0.save(img_name)

def main():
    params = read_params()
    gg = read_gg(params['gg'])
    rounds = [randomize_round(gg, n) for n in range(params['rounds'])]
    for index,round in enumerate(rounds):
        generate_qr(round, params['app_ver'], params['max_crew_size'], index)

if __name__ == '__main__':
    main()
    