from env import Environment
from model import DQN, ReplayBuffer

MAX_BUFFER = 50000
MIN_BUFFER = 5000
TARGET_UPDATE_FREQ = 50
TRAIN_FREQ = 5

replay_buffer = ReplayBuffer(MAX_BUFFER, MIN_BUFFER)
model = DQN()
env = Environment()
# model.epsilon = 0

while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, n_state = env.step(action)
        replay_buffer.push([state, action, n_state, reward, env.over])
        state = n_state

        if replay_buffer.trainable:
            if not env.step_count % TRAIN_FREQ:
                model.train(replay_buffer.sample(model.BATCH_SIZE))
            model.decay_epsilon()
            if not env.step_count % TARGET_UPDATE_FREQ:
                model.update_target()

        print('epsilon:', model.epsilon, 'reward:', reward)

model.save('model2/model')
env.save('model2/r_hist')
