import random
from models.employee import Player


class TrainingSystem:
    TRAINING_PROGRAMS = {
        'shooting': {'ability_impact': 1.5, 'injury_risk': 0.15},
        'tactics': {'ability_impact': 0.8, 'teamwork_impact': 2}
    }

    def conduct_training(self, players: List[Player], program: str) -> Dict:
        if program not in self.TRAINING_PROGRAMS:
            raise ValueError("无效的训练项目")

        params = self.TRAINING_PROGRAMS[program]
        results = {
            'injured_players': [],
            'ability_gains': 0
        }

        for player in players:
            if random.random() < params['injury_risk']:
                results['injured_players'].append(player.name)
                player.injured = True
            else:
                player.ability += params['ability_impact']
                results['ability_gains'] += params['ability_impact']

        return results