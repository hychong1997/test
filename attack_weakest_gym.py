import argparse
import rule_based_env as dsc
import time
from tqdm import tqdm
parser = argparse.ArgumentParser()
parser.add_argument('--ip', help="server ip", default='192.168.230.1')
parser.add_argument('--port', help="server port", type=int, default=11111)
parser.add_argument('--frame-skip', type=int, default=5)
parser.add_argument('--speed', type=int, default=0)
vars_dict = vars(parser.parse_args())


def get_weakest(units):
    min_health = float('inf')
    u = None
    for unit in units:
        if unit.health < min_health:
            min_health = unit.health
            u = unit
    return u


env = dsc.RuleBasedEnv(vars_dict["ip"], vars_dict["port"], frame_skip=vars_dict["frame_skip"],
                       speed=vars_dict["speed"])
print("env set up done")

num_win = 0
total_games = 100
env_obs = env.reset()
done = False
begin_time = time.time()
for cycle in tqdm(range(total_games), ncols=50):
    while not done:
        actions = []
        myunits = env_obs.units[0]
        enemyunits = env_obs.units[1]
        for unit in myunits:
            target = get_weakest(enemyunits)
            if target is not None:
                actions.append([unit.id, target.id])

        env_obs, r, done, info = env.step(actions)
        if done:
            if len(env_obs.units[0]) > 0 and len(env_obs.units[1]) == 0:
                num_win += 1
            env_obs = env.reset()

    done = False

print('attack weakest: win rate for %d games is %0.3f' % (total_games, num_win / total_games))
print('cost time:', time.time() - begin_time)  # 30+ seconds
