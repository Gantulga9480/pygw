from env import Environment
from model import DQN

MODEL_NAME = 'model/6_30_11_44_4/model_217_2.69'

# Load model
model = DQN(MODEL_NAME)
# Prepare env
env = Environment()
# Inferense model
model.epsilon = 0

# Mainloop
while env.running:
    state = env.reset()
    while not env.over:
        action = model.predict_action(state)
        reward, state = env.step(action)

        print('action:', action, 'reward:', reward)
