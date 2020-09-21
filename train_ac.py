# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# Apache License 2.0

import argparse

import h5py

from gomoku import agents
from gomoku import rl

def main():
    """example :
    python train_ac.py --learning-agent <path> --agent-out <path> --lr 0.01 --bs 32 <experience paths>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning-agent', required=True)
    parser.add_argument('--agent-out', required=True)
    parser.add_argument('--lr', type=float, default=0.0001)
    parser.add_argument('--clipnorm', type=float, default=1.0)
    parser.add_argument('--bs', type=int, default=32)
    parser.add_argument('experience', nargs='+')

    args = parser.parse_args()

    learning_agent = agents.load_policy_agent(h5py.File(args.learning_agent))
    for exp_filename in args.experience:
        print(f'Training with {exp_filename}...')
        exp_buffer = rl.load_experience(h5py.File(exp_filename))
        learning_agent.train(
            exp_buffer,
            lr=args.lr,
            clipnorm=args.clipnorm,
            batch_size=args.bs
        )

    with h5py.File(args.agent_out, 'w') as updated_agent_outf:
        learning_agent.serialize(updated_agent_outf)

if __name__ == '__main__':
    main()