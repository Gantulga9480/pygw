from env import Environment
from model import DQN, ReplayBuffer

MAX_BUFFER = 6000
MIN_BUFFER = 1000
TARGET_UPDATE_FREQ = 15
TRAIN_FREQ = 3
EPISODE_STEP = 3000
TRAIN_NAME = '6_30_11_44_22_4'

replay_buffer = ReplayBuffer(MAX_BUFFER, MIN_BUFFER)
model = DQN()
env = Environment()
# model.epsilon = 0

r_sum = 0
step_count = 0
episode_count = 0

while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, n_state = env.step(action)

        step_count += 1
        r_sum += reward

        if step_count > EPISODE_STEP:
            env.over = True
            episode_count += 1
            step_count = 0
            avg_reward = round(r_sum/EPISODE_STEP, 2)
            r_sum = 0
            model.save('model/' + TRAIN_NAME + f'/model_{episode_count}_{avg_reward}.h5')

        replay_buffer.push([state, action, n_state, reward, env.over])
        state = n_state

        if replay_buffer.trainable:
            if step_count % TRAIN_FREQ == 0:
                model.train(replay_buffer.sample(model.BATCH_SIZE))
            model.decay_epsilon()
            if model.epsilon == model.MIN_EPSILON:
                model.epsilon = 0.2
            if step_count % TARGET_UPDATE_FREQ == 0:
                model.update_target()

        print('episode:', episode_count, 'epsilon:', model.epsilon, 'reward:', reward)

model.save('model/' + TRAIN_NAME + '/model')
