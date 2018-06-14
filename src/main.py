#!/usr/bin/env python3.6

import dice

from math import ceil


class Glitch:
    NONE = ""
    GLITCH = "glitch"
    CRITICAL = "critical glitch"


class Damage:
    PHYSICAL = 'physical'
    STUN = 'stun'


class Trigger:
    class Command:
        String = 'command'
        DV = 2
    class Contact:
        String = 'contact'
        DV = 1
    class Time:
        String = 'time'
        DV = 2


class Character:
    '''Temp char'''
    Alchemy = 14
    Drain = 10
    Magic = 5


class Preparation(object):


    def __init__(self, char, name, trigger, force, potency, info):
        self.char = char
        self.name = name
        self.trigger = trigger
        self.force = force
        self.potency = potency
        self.info = info


    def __str__(self):
        return '<{} trigger: {}, force: {}, potency: {}>'.format(
            self.name,
            self.trigger.String,
            self.force,
            self.potency)


    def show_work(self):
        out = "{} [{}] =>".format(self.char.Alchemy, self.force)
        if self.info['is_limited']:
            out += " {} successes (limit hit)".format(self.info['p_hits'])
        else:
            out += " {} successes".format(self.info['p_hits'])
        out += " " + self.info['p_glitch']

        print('Pink preparing {} force {}'.format(self.name, self.force))
        print(out)
        print('Pink: {}'.format(self.info['p_results']))
        if self.info['p_glitch']:
            print('Pink {}!'.format(self.info['p_glitch']))
        print('Opp: {}'.format(self.info['opp_results']))
        if self.info['opp_glitch']:
            print('Opp: {}!'.format(self.info['opp_glitch']))
        print('Resist Drain: {}(spell drain) - {}(drain resist net hits)'.format(self.info['drain'], self.info['d_hits']))
        print('Pink: {}'.format(self.info['d_results']))
        if self.info['d_glitch']:
            print('Pink: {}! while resisting'.format(self.info['d_glitch']))
        if self.info['damage'] > 0:
            print('Damage: {} {}'.format(self.info['damage'], self.info['damage_type']))
        print(self)


    @property
    def damage_stun(self):
        dmg = self.info['damage'] if self.info['damage_type'] == Damage.STUN else 0
        if dmg < 0:
            dmg = 0
        return dmg


    @property
    def damage_physical(self):
        dmg = self.info['damage'] if self.info['damage_type'] == Damage.PHYSICAL else 0
        if dmg < 0:
            dmg = 0
        return dmg


    @property
    def damage(self):
        return self.info['damage']


    @property
    def damage_type(self):
        return self.info['damage_type']


class Formula(object):


    def __init__(self, name, dv, bonus=0, link=None):
        self.name = name
        self.dv = dv
        self.link = link
        self.bonus = bonus


    def prepare(self, char, force, trigger):
        # opposed test
        info = {}
        p_results = dice.roll('{}d6s'.format(char.Alchemy + self.bonus))
        p_results.reverse()
        p_hits = get_hits(p_results)
        is_limited = False
        if p_hits >= force:
            is_limited = True
            p_hits = force
        p_glitch = get_glitch(p_hits, p_results)

        opp_results = dice.roll('{}d6s'.format(force))
        opp_results.reverse()
        opp_hits = get_hits(opp_results)
        opp_glitch = get_glitch(opp_hits, opp_results)

        net_hits = p_hits - opp_hits
        potency = net_hits

        # calculate drain
        drain = force - self.dv + trigger.DV
        if drain < 2:
            drain = 2

        # resist drain
        d_results = dice.roll('{}d6s'.format(char.Drain))
        d_results.reverse()
        d_hits = get_hits(d_results)
        d_glitch = get_glitch(d_hits, d_results)
        damage = drain - d_hits

        # check damage type
        damage_type = Damage.STUN
        if p_hits > char.Magic:
            damage_type = Damage.PHYSICAL

        preparation = Preparation(
            char,
            self.name,
            trigger,
            force,
            potency,
            {
                'is_limited': is_limited,
                'p_hits': p_hits,
                'p_results': p_results,
                'p_glitch': p_glitch,
                'opp_results': opp_results,
                'opp_glitch': opp_glitch,
                'drain': drain,
                'd_results': d_results,
                'd_hits': d_hits,
                'd_glitch': d_glitch,
                'damage': damage,
                'damage_type': damage_type,
            })
        return preparation


def is_hit(n):
    if n >= 5:
        return True
    return False


def get_hits(roll):
    '''Return number of hits.'''
    hits = 0
    for res in roll:
        if is_hit(res):
            hits += 1
    return hits


def get_glitch(hits, roll):
    ret = Glitch.NONE
    ones = 0
    half = ceil(len(roll) / 2.0)
    for res in roll:
        if res == 1:
            ones += 1
    if ones > half:
        ret = Glitch.GLITCH
        if hits < 1:
            ret = Glitch.CRITICAL
    return ret


if __name__ == "__main__":

    def more():
        ans = False
        while not ans:
            i = input()
            if i.lower() == 'y':
                ret = True
                ans = True
            elif i.lower() == 'n':
                ret = False
                ans = True
        return ret

    # Known Spells
    analyze_truth = Formula('Analyze Truth', 2, bonus=2)
    armor = Formula('Armor', 2)
    clairvoyance = Formula('Clairvoyance', 3, bonus=2)
    detect_individual = Formula('Detect Individual', 3, bonus=2)
    flamethrower = Formula('Flamethrower', 3)
    heal = Formula('Heal', 4, bonus=2)
    physical_barrier = Formula('Physical Barrier', 1)
    stealth = Formula('Stealth', 2)

    pink = Character

    # Preparations

    # Basic
    p1 = [
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command),
        heal.prepare(pink, 5, Trigger.Command),
        clairvoyance.prepare(pink, 4, Trigger.Command),
        armor.prepare(pink, 3, Trigger.Command),
    ]

    p2 = [
        clairvoyance.prepare(pink, 4, Trigger.Command),
        analyze_truth.prepare(pink, 2, Trigger.Command),
    ]

    p3 = [
        clairvoyance.prepare(pink, 5, Trigger.Command),
    ]

    p4 = [
        heal.prepare(pink, 5, Trigger.Command),
    ]

    p5 = [
        flamethrower.prepare(pink, 4, Trigger.Command),
        heal.prepare(pink, 5, Trigger.Command),
        armor.prepare(pink, 3, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command)
    ]

    p6 = [
        stealth.prepare(pink, 3, Trigger.Contact),
        stealth.prepare(pink, 3, Trigger.Contact),
        stealth.prepare(pink, 3, Trigger.Contact),
        stealth.prepare(pink, 3, Trigger.Contact),
        stealth.prepare(pink, 3, Trigger.Contact),
    ]

    p7 = [
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command)

    ]

    p8 = [
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command),
        flamethrower.prepare(pink, 4, Trigger.Command),
        armor.prepare(pink, 3, Trigger.Command)
    ]

    prepped = []
    print('------')
    for p in p8:
        p.show_work()
        prepped.append(p)
        print('------')
        if not more():
            break

    print('Prep minutes: {}'.format(sum([x.force for x in prepped])))
    print('Total damage:\nStun {} Physical {}'.format(
        sum([x.damage_stun for x in prepped]),
        sum([x.damage_physical for x in prepped])))
    print('\n'.join([str(x) for x in prepped]))
