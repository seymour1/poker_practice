# poker_practice
Simulate Holdem hands at various stages and calculate hand equity for betting practice

python3 practice.py --round {preflop} --num_players {2..9}

The program will randomly generate a hand and board. The objective for the user is to predict, to the nearest percent, what their hand equity is (and therefore the most they should be willing to bet, without additional information).

To make things easy for the user, the user has 100 in chips and the big blind is 1. The user sees their hand, they type in a bet (between 1 and 100 inclusive), and the simulator then shares their hand equity as the "optimal" bet. When the user is finished, they type END which shares the mean squared error of their bets, as well as their top 5 "worst" estimates against their top 5 "best" estimates.

Currently, the user is always first to act. Future updates will include other positions, continuity between betting rounds, and blind/starting chip customization.
