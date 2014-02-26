"""
It's unfortunate that this file is necessary, but having it inline in the file that uses it would just be a ton of
clutter that no one really wants to see.

Having it organized here also makes it very easy to add to later (if more stats are added) or if I want to modify how
they're organized.
"""

stats = (('assists', 'integer'),
         ('barracksKilled', 'integer'),
         ('championsKilled', 'integer'),
         ('combatPlayerScore', 'integer'),
         ('consumablesPurchased', 'integer'),
         ('damageDealtPlayer', 'integer'),
         ('doubleKills', 'integer'),
         ('firstBlood', 'integer'),
         ('gold', 'integer'),
         ('goldEarned', 'integer'),
         ('goldSpent', 'integer'),
         ('item0', 'integer'),
         ('item1', 'integer'),
         ('item2', 'integer'),
         ('item3', 'integer'),
         ('item4', 'integer'),
         ('item5', 'integer'),
         ('item6', 'integer'),
         ('itemsPurchased', 'integer'),
         ('killingSprees', 'integer'),
         ('largestCriticalStrike', 'integer'),
         ('largestKillingSpree', 'integer'),
         ('largestMultiKill', 'integer'),
         ('legendaryItemsCreated', 'integer'),
         ('level', 'integer'),
         ('magicDamageDealtPlayer', 'integer'),
         ('magicDamageDealtToChampions', 'integer'),
         ('magicDamageTaken', 'integer'),
         ('minionsDenied', 'integer'),
         ('minionsKilled', 'integer'),
         ('neutralMinionsKilled', 'integer'),
         ('neutralMinionsKilledEnemyJungle', 'integer'),
         ('neutralMinionsKilledYourJungle', 'integer'),
         ('nexusKilled', 'text'),
         ('nodeCapture', 'integer'),
         ('nodeCaptureAssist', 'integer'),
         ('nodeNeutralize', 'integer'),
         ('nodeNeutralizeAssist', 'integer'),
         ('numDeaths', 'integer'),
         ('numItemsBought', 'integer'),
         ('objectivePlayerScore', 'integer'),
         ('pentaKills', 'integer'),
         ('physicalDamageDealtPlayer', 'integer'),
         ('physicalDamageDealtToChampions', 'integer'),
         ('physicalDamageTaken', 'integer'),
         ('quadraKills', 'integer'),
         ('sightWardsBought', 'integer'),
         ('spell1Cast', 'integer'),
         ('spell2Cast', 'integer'),
         ('spell3Cast', 'integer'),
         ('spell4Cast', 'integer'),
         ('summonSpell1Cast', 'integer'),
         ('summonSpell2Cast', 'integer'),
         ('superMonsterKilled', 'integer'),
         ('team', 'integer'),
         ('teamObjective', 'integer'),
         ('timePlayed', 'integer'),
         ('totalDamageDealt', 'integer'),
         ('totalDamageDealtToChampions', 'integer'),
         ('totalDamageTaken', 'integer'),
         ('totalHeal', 'integer'),
         ('totalPlayerScore', 'integer'),
         ('totalScoreRank', 'integer'),
         ('totalTimeCrowdControlDealt', 'integer'),
         ('totalUnitsHealed', 'integer'),
         ('tripleKills', 'integer'),
         ('trueDamageDealtPlayer', 'integer'),
         ('trueDamageDealtToChampions', 'integer'),
         ('trueDamageTaken', 'integer'),
         ('turretsKilled', 'integer'),
         ('unrealKills', 'integer'),
         ('victoryPointTotal', 'integer'),
         ('visionWardsBought', 'integer'),
         ('wardKilled', 'integer'),
         ('wardPlaced', 'integer'),
         ('win', 'text'))

fellowPlayer = (('championId', 'integer'),
                ('summonerId', 'integer'),
                ('teamId', 'integer'))

game = (('championId', 'integer'),
        ('createDate', 'integer'),
        ('gameId', 'integer'),
        ('gameMode', 'text'),
        ('gameType', 'text'),
        ('invalid', 'text'),
        ('level', 'integer'),
        ('mapId', 'integer'),
        ('spell1', 'integer'),
        ('spell2', 'integer'),
        ('subType', 'text'),
        ('teamId', 'integer'))

def game_db_fields():
    names = []
    types = []

    tname, ttype = _tuple_to_name_type(game)
    names += tname
    types += ttype

    for i in range(11):
        tname, ttype = _tuple_to_name_type(fellowPlayer, prefix='fellowPlayer{}_'.format(i))
        names += tname
        types += ttype

    tname, ttype = _tuple_to_name_type(stats, prefix='stats_')
    names += tname
    types += ttype

    return (names, types)

def _tuple_to_name_type(tuple_list, prefix='', suffix=''):
    """
    Takes a list of two-tuples and returns them in a separated list after adding prefix and suffix.
    """
    names = []
    types = []
    for (name, type) in tuple_list:
        names.append(prefix + name + suffix)
        types.append(type)

    return (names, types)

if __name__ == '__main__':
    name_type = game_db_fields()
    for i in range(len(name_type[0])):
        print(name_type[0][i], name_type[1][i])