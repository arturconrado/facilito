from fastapi import FastAPI
import random
import numpy as np

app = FastAPI()


class LotteryEnvironment:
    def __init__(self):
        self.state = 0

    def step(self, action):
        winning_number = random.randint(1, 10)
        reward = 10 if action == winning_number else -1
        self.state = (self.state + 1) % 10
        return reward, self.state

    def reset(self):
        self.state = 0


class LotteryAgent:
    def __init__(self, environment):
        self.environment = environment
        self.q_table = np.zeros((10, 10))

    def learn(self, episodes=1000, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0,
              exploration_decay=0.995):
        for episode in range(episodes):
            state = self.environment.reset()
            done = False
            while not done:
                if random.uniform(0, 1) < exploration_rate:
                    action = random.randint(0, 9)
                else:
                    action = np.argmax(self.q_table[state])

                reward, next_state = self.environment.step(action + 1)
                done = True

                self.q_table[state, action] = (1 - learning_rate) * self.q_table[state, action] + \
                                              learning_rate * (
                                                          reward + discount_factor * np.max(self.q_table[next_state]))

                state = next_state

            exploration_rate *= exploration_decay

    def get_optimal_strategy(self):
        return np.argmax(self.q_table[0]) + 1


@app.post("/optimize/strategy")
def optimize_strategy():
    environment = LotteryEnvironment()
    agent = LotteryAgent(environment)
    agent.learn()

    strategy = agent.get_optimal_strategy()

    return {"strategy": strategy}
