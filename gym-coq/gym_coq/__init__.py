from gym.envs.registration import register

register(
    id='Coq-v0',
    entry_point='gym_coq.envs:CoqEnv',
)
register(
    id='coq-extrahard-v0',
    entry_point='gym_coq.envs:CoqExtraHardEnv',
)
