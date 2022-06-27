from env import Environment
from model import DQN, ReplayBuffer

MAX_BUFFER = 10000
MIN_BUFFER = 1000
TARGET_UPDATE_FREQ = 500
TRAIN_FREQ = 5

replay_buffer = ReplayBuffer(MAX_BUFFER, MIN_BUFFER)
model = DQN()
env = Environment()
# model.epsilon = 0

r_sum = 0

while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, n_state = env.step(action)
        replay_buffer.push([state, action, n_state, reward, env.over])
        state = n_state

        r_sum += reward

        if replay_buffer.trainable:
            if env.step_count % TRAIN_FREQ == 0:
                model.train(replay_buffer.sample(model.BATCH_SIZE))
            model.decay_epsilon()
            if env.step_count % TARGET_UPDATE_FREQ == 0:
                model.update_target()
                avg_reward = round(r_sum/TARGET_UPDATE_FREQ, 2)
                # model.save(f'model/model_{env.step_count}_{avg_reward}.h5')
                r_sum = 0

        print('epsilon:', model.epsilon, 'reward:', reward)

model.save('model/model')
env.save('model/r_hist')
