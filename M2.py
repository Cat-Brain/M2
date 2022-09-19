# M2, this is a sequel to a mod(made by me, Jordan Baumann) of a game made by Matthew Tabet.
# Go to https://github.com/Matthew-12525/Create-Your-Own-Adventure for the original game, it's super super different.
"""
Hiya, this 'mod' was written by Jordan Baumann (me),
however this all wouldn't of existed without Matthew's original version of the game (link above ^^^).
I hope that you enjoy this experience, and if you want, maybe you'll even mod this mod! =]
"""

from copy import deepcopy # This lets us pass lists that aren't references.
from enum import Enum # This lets me use enum classes, and they look nice. =]
from math import *
import random
import time
from colorama import Fore
from colorama import Style














#Classes:

class InflictionType(Enum):
    POISON = 0
    BLEED = 1
    BURNING = 2
    DEADLY_HUG = 3
    STUN = 4
    WET = 5
    STRENGHTEN = 6
    # Insert more status effects here.



class Infliction:
    effect : InflictionType

    def __init__(self, effect : InflictionType):
        self.effect = effect

    def FindDamage(self):
        if self.effect ==  InflictionType.POISON:
            return 2
        elif self.effect == InflictionType.BLEED:
            return 3
        elif self.effect == InflictionType.BURNING:
            return 10
        elif self.effect == InflictionType.DEADLY_HUG:
            return 1
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 0
        elif self.effect == InflictionType.STRENGHTEN:
            return 0
        else:
            return 0

    def DeathDamage(self):
        if self.effect ==  InflictionType.POISON:
            return 2
        elif self.effect == InflictionType.BLEED:
            return 1
        elif self.effect == InflictionType.BURNING:
            return 5
        elif self.effect == InflictionType.DEADLY_HUG:
            return 10
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 0
        elif self.effect == InflictionType.STRENGHTEN:
            return 0
        else:
            return 0

    def FindDamageReduction(self):
        if self.effect ==  InflictionType.POISON:
            return 0
        elif self.effect == InflictionType.BLEED:
            return 0
        elif self.effect == InflictionType.BURNING:
            return 0
        elif self.effect == InflictionType.DEADLY_HUG:
            return 0
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 15
        elif self.effect == InflictionType.STRENGHTEN:
            return -10
        else:
            return 0

    def FindName(self):
        if self.effect ==  InflictionType.POISON:
            return "poison"
        elif self.effect == InflictionType.BLEED:
            return "bleed"
        elif self.effect == InflictionType.BURNING:
            return "burning"
        elif self.effect == InflictionType.DEADLY_HUG:
            return "deadly hug"
        elif self.effect == InflictionType.STUN:
            return "stun"
        elif self.effect == InflictionType.WET:
            return "wet"
        elif self.effect == InflictionType.STRENGHTEN:
            return "strengthen"
        else:
            return "NULL INFLICTION TYPE"
    
    def AccumulationType(self): # 0 = independant, 1 = yes stacking, 2 = stacks and accumulates duration, 3 = stacks length but keeps same damage.
        if self.effect ==  InflictionType.POISON:
            return 1
        elif self.effect == InflictionType.BLEED:
            return 2
        elif self.effect == InflictionType.BURNING:
            return 1
        elif self.effect == InflictionType.DEADLY_HUG:
            return 0
        elif self.effect == InflictionType.STUN:
            return 2
        elif self.effect == InflictionType.WET:
            return 2
        elif self.effect == InflictionType.STRENGHTEN:
            return 0
        else:
            return 0



class StatusEffect:
    effect : Infliction
    durationLeft : int
    shouldBeDestroyed : bool

    def __init__(self, effect : InflictionType, duration : int):
        self.effect = Infliction(effect)
        self.durationLeft = duration
        self.shouldBeDestroyed = False

    def Update(self):
        self.durationLeft -= 1
        if self.durationLeft <= 0:
            self.shouldBeDestroyed = True
            return self.DeathDamage()
        return self.FindDamage()

    def FindDamage(self):
        return self.effect.FindDamage()

    def DeathDamage(self):
        return self.effect.DeathDamage()

    def Reduction(self):
        return self.effect.FindDamageReduction()

    def Name(self):
        return self.effect.FindName()



class Ailment: # DON'T USE FOR MOST CODE, MADE FOR QOL NOT ACTUAL USE.
    inflictor : int

    def __init__(self, statusEffect : StatusEffect, inflictor : int):
        self.statusEffect = statusEffect
        inflictor = inflictor

    def Update(self):
        return self.statusEffect.Update()

    def FindDamage(self):
        return self.statusEffect.effect.FindDamage()

    def DeathDamage(self):
        return self.statusEffect.effect.DeathDamage()

    def Reduction(self):
        return self.statusEffect.effect.FindDamageReduction()

    def Name(self):
        return self.statusEffect.effect.FindName()



class AilmentStackBase(StatusEffect):
    inflictors : int
    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.inflictors = [ailment.inflictor]
    
    def AddStatusEffect(self, statusEffect : StatusEffect):
        print("You shouldn't be seeing this, AilmentStackBase : AddStatusEffect virtal function.")


#region Status Stack sub-classes

class StatusStackType0(AilmentStackBase): # No stacking pretty much. Think of all status effect in M1
    statuses : StatusEffect
    inflictors : int

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statuses = [ailment.statusEffect]
        self.inflictors = [ailment.inflictor]
    
    def AddStatusEffect(self, ailment : Ailment):
        self.statuses.append(ailment.statusEffect)
        self.inflictors.append(ailment.inflictor)

class StatusStackType1(AilmentStackBase): # No stacking pretty much. Think of all status effect in M1
    statuses : StatusEffect
    inflictors : int

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statuses = [ailment.statusEffect]
        self.inflictors = [ailment.inflictor]
    
    def AddStatusEffect(self, ailment : Ailment):
        self.statuses.append(ailment.statusEffect)
        self.inflictors.append(ailment.inflictor)

class StatusStackType2(AilmentStackBase): # No stacking pretty much. Think of all status effect in M1
    statuses : StatusEffect
    inflictors : int

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statuses = [ailment.statusEffect]
        self.inflictors = [ailment.inflictor]
    
    def AddStatusEffect(self, ailment : Ailment):
        self.statuses.append(ailment.statusEffect)
        self.inflictors.append(ailment.inflictor)

class StatusStackType3(AilmentStackBase): # No stacking pretty much. Think of all status effect in M1
    statuses : StatusEffect
    inflictors : int

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statuses = [ailment.statusEffect]
        self.inflictors = [ailment.inflictor]
    
    def AddStatusEffect(self, ailment : Ailment):
        self.statuses.append(ailment.statusEffect)
        self.inflictors.append(ailment.inflictor)


#endregion
statusStackTypeArray = [StatusStackType0, StatusStackType1, StatusStackType2, StatusStackType3]



class Ailments:
    stacks : AilmentStackBase
    
    def __init__(self):
        self.stacks = []
    
    def AddStatusEffect(self, statusEffect : StatusEffect):
        for i in range(len(self.stacks)):
            if self.stacks[i].effect == statusEffect.effect:
                self.stacks[i].AddStatusEffect(statusEffect)
                return
        self.stacks.append(statusStackTypeArray[statusEffect.effect.AccumulationType()](statusEffect))
    




class Hit:
    damage : int
    inflictions : StatusEffect
    attacker : int

    def __init__(self, damage : int, inflictions : StatusEffect, attacker : int):
        self.damage = damage
        self.inflictions = inflictions
        self.attacker = attacker



class Attack:
    procs : StatusEffect
    procChances : int # Percent
    damage : int
    damageRand : int
    selfProcs : StatusEffect
    selfProcChances : int # Percent
    selfDamage : int
    selfDamageRand : int
    length : int
    timeSinceStart : int
    name : str

    def __init__(self, procs : StatusEffect, procChances : int, damage : int, damageRand : int,\
        selfProcs : StatusEffect, selfProcChances : int, selfDamage : int, selfDamageRand : int, summons, length : int, name : int):
        self.procs = procs
        self.procChances = procChances
        self.damage = damage
        self.damageRand = damageRand
        self.selfProcs = selfProcs
        self.selfProcChances = selfProcChances
        self.selfDamage = selfDamage
        self.selfDamageRand = selfDamageRand
        copyOfSummons = []
        for summon in summons:
            copyOfSummons.append(deepcopy(summon))
        self.summons = copyOfSummons
        self.length = length
        self.name = name
        self.timeSinceStart = 0

    def RollDamage(self, currentIndex : int, damageReduction : int):
        inflictions = []
        for i in range(len(self.procs)):
            if random.randint(1, 100) <= self.procChances[i]:
                inflictions.append(self.procs[i])
        selfInflictions = []
        for i in range(len(self.selfProcs)):
            if random.randint(1, 100) <= self.selfProcChances[i]:
                selfInflictions.append(self.selfProcs[i])

        unModifiedDamage = max(0, random.randint(self.damage - self.damageRand, self.damage + self.damageRand))
        unModifiedSelfDamage = max(0, random.randint(self.selfDamage - self.selfDamageRand, self.selfDamage + self.selfDamageRand))
        return Hit(max(0, unModifiedDamage - damageReduction), inflictions, currentIndex), unModifiedDamage,\
            Hit(max(0, unModifiedSelfDamage - damageReduction), selfInflictions, currentIndex), unModifiedSelfDamage



class Enemy:
    inflictions : StatusEffect
    inflictionAttackers : int
    health : int
    maxHealth : int
    activeAttack : int
    attacks : Attack
    name : str
    leech : float
    summoned : bool

    def __init__(self, health : int, maxHealth : int, attacks : Attack, name : str, leech : float):
        self.inflictions = []
        self.inflictionAttackers = []
        self.health = health
        self.maxHealth = maxHealth
        self.activeAttack = 0
        self.attacks = deepcopy(attacks)
        self.name = name
        self.leech = leech
        self.summoned = False

    def CurrentAttack(self):
        return self.attacks[self.activeAttack]

    def FindNewAttack(self):
        self.attacks[self.activeAttack].timeSinceStart = 0
        self.activeAttack = random.randint(0, len(self.attacks) - 1)
        self.attacks[self.activeAttack].timeSinceStart = 1
        if self.CurrentAttack().length - self.CurrentAttack().timeSinceStart > 0:
            print(self.name + " starts preparing " + self.CurrentAttack().name + " It'll be done in " + str(self.CurrentAttack().length - self.CurrentAttack().timeSinceStart + 1) + " turns.")
        else:
            print(self.name + " starts preparing " + self.CurrentAttack().name + " It'll be done next turn.")

    def FindDamageReduction(self):
        damageReduction = 0
        for infliction in self.inflictions:
            damageReduction += infliction.Reduction()
        return damageReduction

    def TakeTurn(self, currentIndex : int):
        hit : Hit
        enemiesBorn = []

        if self.CurrentAttack().length <= self.CurrentAttack().timeSinceStart:
            hit, unmodifiedDamage, selfHit, unmodifiedSelfDamage = self.CurrentAttack().RollDamage(currentIndex, self.FindDamageReduction())
            enemiesBorn = deepcopy(self.CurrentAttack().summons)
            if hit.damage != 0 or hit.inflictions != []:
                if unmodifiedDamage != hit.damage:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage. It would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage.")
                for infliction in hit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " for " + str(infliction.durationLeft) + " turns.")
            else:
                if unmodifiedDamage > 0:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n" + \
self.name + " misses, but it would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                elif self.CurrentAttack().damage != 0 or self.CurrentAttack().damageRand != 0:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n" + \
self.name + " misses.")
                # else maybe print something.

            if selfHit.damage != 0 or selfHit.inflictions != []:
                healOrDeal = "deals " + str(selfHit.damage) + " damage to"
                if selfHit.damage < 0:
                    healOrDeal = "heals for " + str(-selfHit.damage) + " health points on"

                if unmodifiedSelfDamage != selfHit.damage:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve. It would've done " + str(unmodifiedSelfDamage) + " if it weren't for inflictions.")
                else:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve.")
                for infliction in selfHit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " on themselve for " + str(infliction.durationLeft) + " turns.")
                self.ApplyHit(selfHit)

            self.FindNewAttack()


        else:
            hit = Hit(0, [], currentIndex)
            if self.CurrentAttack().length - self.CurrentAttack().timeSinceStart > 1:
                print(self.name + " continues to prepare their " + self.CurrentAttack().name + ". They have " + str(self.CurrentAttack().length - self.CurrentAttack().timeSinceStart) + " turns left.")
            else:
                print(self.name + " continues to prepare their " + self.CurrentAttack().name + ". They will be done next turn.")
            self.attacks[self.activeAttack].timeSinceStart += 1

        return hit, enemiesBorn

    def ApplyHit(self, hit : Hit):
        self.health -= hit.damage
        self.inflictions.extend(deepcopy(hit.inflictions))
        self.inflictionAttackers.extend([hit.attacker] * len(hit.inflictions))

    def UpdateInflictions(self):
        destroyedThisFrame = 0

        damageFromSources = [0] * len(self.inflictionAttackers)

        respectiveNames = [""] * len(self.inflictionAttackers)
        for i in range(len(self.inflictions)):
            respectiveNames[i] = self.inflictions[i].Name()

        orinalInflictionAttackers = deepcopy(self.inflictionAttackers)

        for i in range(len(self.inflictions)):
            damage = self.inflictions[i - destroyedThisFrame].Update()
            self.health -= damage
            damageFromSources[i] += damage

            if self.inflictions[i - destroyedThisFrame].shouldBeDestroyed:
                if damage > 0:
                    print(self.name + "'s " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed but it did " + str(damage) + " damage this turn.")
                else:
                    print(self.name + "'s " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed and did no damage this turn.")
                del self.inflictions[i - destroyedThisFrame]
                del self.inflictionAttackers[i - destroyedThisFrame]
                destroyedThisFrame += 1
            else:
                damageThisTurn = ""
                reductionThisTurn = ""
                durationThisTurn = "It'll be gone next turn."
                if damage > 0:
                    damageThisTurn = "It did " + str(damage) + " damage this turn.\n"
                reduction = self.inflictions[i - destroyedThisFrame].Reduction()
                if reduction > 0:
                    reductionThisTurn = "It will reduce physical attacks by " + str(reduction) + ".\n"
                elif reduction < 0:
                    reductionThisTurn = "It will increase physical attacks by " + str(-reduction) + ".\n"
                duration = self.inflictions[i - destroyedThisFrame].durationLeft
                if duration > 1:
                    durationThisTurn = "It'll be gone in " + str(duration) + " turns."
                print(self.name + " is inflicted with " + self.inflictions[i - destroyedThisFrame].Name() + ".\n" + damageThisTurn +  reductionThisTurn + durationThisTurn)

        return orinalInflictionAttackers, damageFromSources, respectiveNames

    def IsStunned(self):
        for infliction in self.inflictions:
            if infliction.effect.effect == InflictionType.STUN:
                return True
        return False



class Weapon:
    activeAttack : int
    attacks : Attack
    name : str
    leech : float

    def __init__(self, attacks : Attack, name : str, leech : float):
        self.activeAttack = 0
        self.attacks = deepcopy(attacks)
        self.name = name
        self.leech = leech

    def CurrentAttack(self):
        return self.attacks[self.activeAttack]

    def ChangeAttackTo(self, newAttack : int):
        self.attacks[self.activeAttack].timeSinceStart = 0
        self.activeAttack = newAttack
        self.attacks[self.activeAttack].timeSinceStart = 1
        if self.CurrentAttack().length - self.CurrentAttack().timeSinceStart > 0:
            print("Max starts preparing " + self.CurrentAttack().name + " It'll be done in " + str(self.CurrentAttack().length - self.CurrentAttack().timeSinceStart + 1) + " turns.")
        else:
            print("Max starts preparing " + self.CurrentAttack().name + " It'll be done next turn.")

    def SwitchAttacks(self, startingText : str, nevermindable : bool):
            turnDialogue = startingText + "'" + self.attacks[0].name + "' "
            for attack in range(len(self.attacks) - 1):
                turnDialogue += "or '" + self.attacks[attack + 1].name + "' "

            if nevermindable:
                turnDialogue += " or 'nevermind'? "

            prompt = input(turnDialogue)

            inputedAttack = 0

            badInput = True
            
            if prompt == "nevermind" and nevermindable:
                badInput = False
                inputedAttack = self.activeAttack

            for currentAttack in range(len(self.attacks)):
                if prompt == self.attacks[currentAttack].name:
                    badInput = False
                    inputedAttack = currentAttack

            while badInput:
                prompt = input("That won't work this time! Do you want to " + turnDialogue)
                badInput = ((prompt != "nevermind") or (not nevermindable))
                for currentAttack in range(len(self.attacks)):
                    if prompt == self.attacks[currentAttack].name:
                        badInput = False
                        inputedAttack = currentAttack
            
            self.ChangeAttackTo(inputedAttack)

    def LearnAttack(self, attack : Attack):
        self.attacks.append(attack)

    def KnowsAttack(self, name : str):
        for attack in self.attacks:
            if attack.name == name:
                return True
        return False



class Unit:
    ailments : Ailments
    inflictions : StatusEffect
    inflictionAttackers : int
    maxHealth : int
    currentHealth : int
    weapon : Weapon
    deathMessage : str

    def __init__(self, maxHealth : int, deathMessage : str):
        self.inflictions = []
        self.inflictionAttackers = []
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
        self.deathMessage = deathMessage

    def FindDamageReduction(self):
        damageReduction = 0
        for infliction in self.inflictions:
            damageReduction += infliction.Reduction()
        return damageReduction

    def TakeTurn(self):
        hit : Hit

        if self.weapon.CurrentAttack().length <= self.weapon.CurrentAttack().timeSinceStart:
            hit, unmodifiedDamage, selfHit, unmodifiedSelfDamage = self.weapon.CurrentAttack().RollDamage(0, self.FindDamageReduction())
            if hit.damage != 0 or hit.inflictions != []:
                if unmodifiedDamage != hit.damage:
                    print("Max uses their " + self.weapon.name + " and does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage. It would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print("Max uses their " + self.weapon.name + " and does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage.")
                for infliction in hit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " for " + str(infliction.durationLeft) + " turns.")
            else:
                if unmodifiedDamage > 0:
                    print("Max's " + self.weapon.name + " misses, but it would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print("Max's " + self.weapon.name + " misses.")
            
            self.weapon.attacks[self.weapon.activeAttack].timeSinceStart = 0

            if selfHit.damage != 0 or selfHit.inflictions != []:
                healOrDeal = "deals " + str(selfHit.damage) + " damage to"
                if selfHit.damage < 0:
                    healOrDeal = "heals for " + str(-selfHit.damage) + " health points on"

                if unmodifiedSelfDamage != selfHit.damage:
                    print("Max does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve. It would've done " + str(unmodifiedSelfDamage) + " if it weren't for inflictions.")
                else:
                    print("Max does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve.")
                for infliction in selfHit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " on themselve for " + str(infliction.durationLeft) + " turns.")
                self.ApplyHit(selfHit)


        else:
            hit = Hit(0, [], 0)
            if self.weapon.CurrentAttack().length - self.weapon.CurrentAttack().timeSinceStart > 1:
                print("Max continues to prepare their " + self.weapon.name + "'s " + self.weapon.CurrentAttack().name + ". They have " + str(self.weapon.CurrentAttack().length - self.weapon.CurrentAttack().timeSinceStart) + " turns left.")
            else:
                print("Max continues to prepare their " + self.weapon.name + "'s " + self.weapon.CurrentAttack().name + ". They will be done next turn.")
            
        self.weapon.attacks[self.weapon.activeAttack].timeSinceStart += 1

        return hit

    def ApplyHit(self, hit : Hit, dodged : bool):
        self.currentHealth -= hit.damage
        for infliction in deepcopy(hit.inflictions):
            if infliction.effect.effect != InflictionType.STUN or not dodged:
                self.inflictions.append(infliction)
            else:
                halfTimeInfliction = infliction
                halfTimeInfliction.durationLeft = int(floor(float(halfTimeInfliction.durationLeft) / 2))
                self.inflictions.append(halfTimeInfliction)
                print("Because you blocked get stunned for half as long. Which is in this case " + str(halfTimeInfliction.durationLeft) + " turn.")
        self.inflictionAttackers.extend([hit.attacker] * len(hit.inflictions))

    def UpdateInflictions(self):
        destroyedThisFrame = 0

        damageFromSources = [0] * len(self.inflictionAttackers)

        respectiveNames = [""] * len(self.inflictionAttackers)
        for i in range(len(self.inflictions)):
            respectiveNames[i] = self.inflictions[i].Name()

        orinalInflictionAttackers = deepcopy(self.inflictionAttackers)

        for i in range(len(self.inflictions)):
            damage = self.inflictions[i - destroyedThisFrame].Update()
            self.currentHealth -= damage
            damageFromSources[i] += damage

            if self.inflictions[i - destroyedThisFrame].shouldBeDestroyed:
                if damage > 0:
                    print("Your " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed but it did " + str(damage) + " damage this turn.")
                else:
                    print("Your " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed and did no damage this turn.")
                del self.inflictions[i - destroyedThisFrame]
                del self.inflictionAttackers[i - destroyedThisFrame]
                destroyedThisFrame += 1

            else:
                damageThisTurn = ""
                reductionThisTurn = ""
                durationThisTurn = "It'll be gone next turn."
                if damage > 0:
                    damageThisTurn = "It did " + str(damage) + " damage this turn.\n"
                reduction = self.inflictions[i - destroyedThisFrame].Reduction()
                if reduction > 0:
                    reductionThisTurn = "It will reduce physical attacks by " + str(reduction) + ".\n"
                elif reduction < 0:
                    reductionThisTurn = "It will increase physical attacks by " + str(-reduction) + ".\n"
                duration = self.inflictions[i - destroyedThisFrame].durationLeft
                if duration > 1:
                    durationThisTurn = "It'll be gone in " + str(duration) + " turns."
                print("Max is inflicted with " + self.inflictions[i - destroyedThisFrame].Name() + ".\n" + damageThisTurn +  reductionThisTurn + durationThisTurn)
        
        return orinalInflictionAttackers, damageFromSources, respectiveNames

    def IsStunned(self):
        for infliction in self.inflictions:
            if infliction.effect.effect == InflictionType.STUN:
                return True
        return False



class Player:
    ailments : Ailments
    inflictions : StatusEffect
    inflictionAttackers : int
    maxHealth : int
    currentHealth : int
    weapon : Weapon
    deathMessage : str

    def __init__(self, maxHealth : int, deathMessage : str):
        self.inflictions = []
        self.inflictionAttackers = []
        self.maxHealth = maxHealth
        self.currentHealth = maxHealth
        self.deathMessage = deathMessage

    def FindDamageReduction(self):
        damageReduction = 0
        for infliction in self.inflictions:
            damageReduction += infliction.Reduction()
        return damageReduction

    def TakeTurn(self):
        hit : Hit

        if self.weapon.CurrentAttack().length <= self.weapon.CurrentAttack().timeSinceStart:
            hit, unmodifiedDamage, selfHit, unmodifiedSelfDamage = self.weapon.CurrentAttack().RollDamage(0, self.FindDamageReduction())
            if hit.damage != 0 or hit.inflictions != []:
                if unmodifiedDamage != hit.damage:
                    print("Max uses their " + self.weapon.name + " and does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage. It would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print("Max uses their " + self.weapon.name + " and does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage.")
                for infliction in hit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " for " + str(infliction.durationLeft) + " turns.")
            else:
                if unmodifiedDamage > 0:
                    print("Max's " + self.weapon.name + " misses, but it would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print("Max's " + self.weapon.name + " misses.")
            
            self.weapon.attacks[self.weapon.activeAttack].timeSinceStart = 0

            if selfHit.damage != 0 or selfHit.inflictions != []:
                healOrDeal = "deals " + str(selfHit.damage) + " damage to"
                if selfHit.damage < 0:
                    healOrDeal = "heals for " + str(-selfHit.damage) + " health points on"

                if unmodifiedSelfDamage != selfHit.damage:
                    print("Max does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve. It would've done " + str(unmodifiedSelfDamage) + " if it weren't for inflictions.")
                else:
                    print("Max does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve.")
                for infliction in selfHit.inflictions:
                    print("This attack inflicts " + infliction.Name() + " on themselve for " + str(infliction.durationLeft) + " turns.")
                self.ApplyHit(selfHit)


        else:
            hit = Hit(0, [], 0)
            if self.weapon.CurrentAttack().length - self.weapon.CurrentAttack().timeSinceStart > 1:
                print("Max continues to prepare their " + self.weapon.name + "'s " + self.weapon.CurrentAttack().name + ". They have " + str(self.weapon.CurrentAttack().length - self.weapon.CurrentAttack().timeSinceStart) + " turns left.")
            else:
                print("Max continues to prepare their " + self.weapon.name + "'s " + self.weapon.CurrentAttack().name + ". They will be done next turn.")
            
        self.weapon.attacks[self.weapon.activeAttack].timeSinceStart += 1

        return hit

    def ApplyHit(self, hit : Hit, dodged : bool):
        self.currentHealth -= hit.damage
        for infliction in deepcopy(hit.inflictions):
            if infliction.effect.effect != InflictionType.STUN or not dodged:
                self.inflictions.append(infliction)
            else:
                halfTimeInfliction = infliction
                halfTimeInfliction.durationLeft = int(floor(float(halfTimeInfliction.durationLeft) / 2))
                self.inflictions.append(halfTimeInfliction)
                print("Because you blocked get stunned for half as long. Which is in this case " + str(halfTimeInfliction.durationLeft) + " turn.")
        self.inflictionAttackers.extend([hit.attacker] * len(hit.inflictions))

    def UpdateInflictions(self):
        destroyedThisFrame = 0

        damageFromSources = [0] * len(self.inflictionAttackers)

        respectiveNames = [""] * len(self.inflictionAttackers)
        for i in range(len(self.inflictions)):
            respectiveNames[i] = self.inflictions[i].Name()

        orinalInflictionAttackers = deepcopy(self.inflictionAttackers)

        for i in range(len(self.inflictions)):
            damage = self.inflictions[i - destroyedThisFrame].Update()
            self.currentHealth -= damage
            damageFromSources[i] += damage

            if self.inflictions[i - destroyedThisFrame].shouldBeDestroyed:
                if damage > 0:
                    print("Your " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed but it did " + str(damage) + " damage this turn.")
                else:
                    print("Your " + self.inflictions[i - destroyedThisFrame].Name() + " infliction has been destroyed and did no damage this turn.")
                del self.inflictions[i - destroyedThisFrame]
                del self.inflictionAttackers[i - destroyedThisFrame]
                destroyedThisFrame += 1

            else:
                damageThisTurn = ""
                reductionThisTurn = ""
                durationThisTurn = "It'll be gone next turn."
                if damage > 0:
                    damageThisTurn = "It did " + str(damage) + " damage this turn.\n"
                reduction = self.inflictions[i - destroyedThisFrame].Reduction()
                if reduction > 0:
                    reductionThisTurn = "It will reduce physical attacks by " + str(reduction) + ".\n"
                elif reduction < 0:
                    reductionThisTurn = "It will increase physical attacks by " + str(-reduction) + ".\n"
                duration = self.inflictions[i - destroyedThisFrame].durationLeft
                if duration > 1:
                    durationThisTurn = "It'll be gone in " + str(duration) + " turns."
                print("Max is inflicted with " + self.inflictions[i - destroyedThisFrame].Name() + ".\n" + damageThisTurn +  reductionThisTurn + durationThisTurn)
        
        return orinalInflictionAttackers, damageFromSources, respectiveNames

    def IsStunned(self):
        for infliction in self.inflictions:
            if infliction.effect.effect == InflictionType.STUN:
                return True
        return False



class Settings:
    sleepTime : int

    def __init__(self, sleepTime : int):
        self.sleepTime = sleepTime

        




















def ChooseDestination(possibilities : str, possibleAnswers : str, firstInputText, badInputText): # Must be in string form even if result should be numeric
    text = ""
    for currentPossibility in possibilities:
        text += currentPossibility + "\n"
    result = input(text + firstInputText).lower()
    badInput = True
    for currentPossibility in possibleAnswers:
        badInput &= currentPossibility != result
    while badInput:
        result = input(text + badInputText).lower()
        for currentPossibility in possibleAnswers:
            badInput &= currentPossibility != result
    return result



def FindSettings():
    global currentSettings
    prompt = input("How many seconds do you want to wait after key events('default' = 1) ").lower()
    badInput = not prompt.isnumeric()
    if not badInput:
        badInput = int(prompt) < 0
    badInput &= prompt != "default"
    while badInput:
        prompt = input("It has to be a number or 'default'. How many seconds do you want to wait after key events('default' = 1) ")
        badInput = not prompt.isnumeric()
        if not badInput:
            badInput = int(prompt) < 0
        badInput &= prompt != "default"
    if prompt == "default":
        currentSettings = Settings(1)
    else:
        currentSettings = Settings(int(prompt))



def CharacterSelect():
    print("Hi!")


























#Variables and game:

#Globalizing variables

specialFightEnding = False
specialFightEndingMonsters = []
player : Player
currentSettings : Settings

#Constant variables:
#Attacks 
#The syntax for a status effect is:
#StatusEffect(InflictionType.YOURINFLICTION, how long you want it to last)
#The syntax for an attacks is:
#Attack([Status effects], [chance of each status effect happening], damage, damage randomness (how far from the original value the actual value can be), [self inflictions], [self infliction procs], self damage, self damage randomness, [summons], turns to do, name)
#First up is the attacks that are required to be early.
fireBreath = Attack([StatusEffect(InflictionType.BURNING, 2)], [100], 0, 0, [], [], 0, 0, [], 3, "fire breath")
heavyBite = Attack([], [], 50, 0, [], [], 0, 0, [], 4, "heavy bite")
#Enemies that must be declared early.
joshroHead = Enemy(25, 50, [fireBreath, heavyBite], "Joshro Head", 0.5)
#Normal attacks.
clubBash = Attack([StatusEffect(InflictionType.STUN, 2)], [100], 25, 10, [], [], 0, 0, [], 3, "club bash")
punch = Attack([], [], 15, 15, [], [], 0, 0, [], 1, "punch")
heavyPunch = Attack([StatusEffect(InflictionType.STUN, 2)], [75], 25, 25, [], [], 0, 0, [], 2, "heavy punch")
quickStab = Attack([StatusEffect(InflictionType.POISON, 3)], [50], 5, 5, [], [], 0, 0, [], 1, "quick stab")
rockThrow = Attack([StatusEffect(InflictionType.STUN, 1)], [25], 5, 5, [], [], 0, 0, [], 1, "rock throw")
slimeHug = Attack([StatusEffect(InflictionType.DEADLY_HUG, 3)], [100], 0, 0, [], [], 0, 0, [], 1, "slime hug")
slimeSpike = Attack([StatusEffect(InflictionType.BLEED, 3)], [100], 5, 0, [], [], 0, 0, [], 1, "slime spike")
arrowShoot = Attack([StatusEffect(InflictionType.BURNING, 3), StatusEffect(InflictionType.POISON, 8)], [100, 100], 35, 10, [], [], 0, 0, [], 3, "shoot arrow")
chokeHold = Attack([StatusEffect(InflictionType.STUN, 1)], [75], 5, 5, [], [], 0, 0, [], 1, "choke hold")
deepCut = Attack([StatusEffect(InflictionType.BLEED, 15), StatusEffect(InflictionType.BLEED, 15), StatusEffect(InflictionType.BLEED, 15)], [100, 50, 25], 0, 0, [], [], 0, 0, [], 1, "deep cut")
finisher = Attack([], [], 20, 0, [], [], 0, 0, [], 1, "finisher")
heavyBlow = Attack([], [], 100, 0, [], [], 0, 0, [], 5, "heavy blow")
quickAttack = Attack([], [], 35, 0, [], [], 0, 0, [], 2, "quick attack")
heaviestBlow = Attack([], [], 125, 0, [], [], 0, 0, [], 6, "heaviest blow")
splash = Attack([StatusEffect(InflictionType.WET, 5)], [100], 3, 3, [], [], 0, 0, [], 1, "splash")
quickClubBash = Attack([StatusEffect(InflictionType.STUN, 2)], [75], 10, 10, [], [], 0, 0, [], 2, "quick club bash")
bite = Attack([StatusEffect(InflictionType.POISON, 4), StatusEffect(InflictionType.BLEED, 4)], [5, 5], 5, 5, [], [], 0, 0, [], 2, "bite")
scratch = Attack([StatusEffect(InflictionType.BLEED, 4)], [25], 15, 5, [], [], 0, 0, [], 1, "scratch")
spare = Attack([], [], 0, 0, [], [], 0, 0, [], 1, "spare")
growHead = Attack([], [], 0, 0, [], [], 0, 0, [joshroHead], 2, "grow head")
ultraFireBreath = Attack([StatusEffect(InflictionType.BURNING, 3)], [100], 0, 0, [], [], 0, 0, [], 1, "ultra fire breath")

# The syntax for enemies is:
# Enemy(start health, max health, [attack1, attack2, ...], "name", leech amount 0 to 1 work best
joshrosBody = Enemy(300, 300, [growHead], "Joshro's Body", 0.0)
ogre = Enemy(100, 100, [clubBash, punch], "Ogre", 0.0)
goblin = Enemy(100, 100, [quickStab, rockThrow], "Goblin", 0.0)
slime = Enemy(25, 50, [slimeHug], "Pet Slime", 1.0)
troll = Enemy(125, 125, [quickClubBash, splash], "troll", 0.0)
mutant = Enemy(200, 200, [punch, heavyPunch], "mutant", 0.0)
rat = Enemy(100, 200, [bite, scratch], "Rat", 0.25)
babyRat = Enemy(25, 50, [bite, scratch, splash], "Baby Rat", 0.5)
guard = Enemy(200, 200, [heavyBlow, quickAttack], "Unloyal Guard", 0.0)

def Main():
    global player, joshroHead, specialFightEnding, restart, currentSettings
    restart = False
    player = CharacterSelect()
















print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")
gameRunning = True
while gameRunning:
    result = ChooseDestination(["Begin", "Settings", "End game"], ["begin", "settings", "end game"], "Where do you want to go? ", "It must be one of the 3 options above, sorry. Where do you want to go? ")
    if result == "begin":
        Main()
    elif result == "settings":
        FindSettings()
    else:
        gameRunning = False
