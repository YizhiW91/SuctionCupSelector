from enum import Enum


class SuctionCup(Enum):
    any = 0
    small = 1
    medium = 2
    large_type1 = 3
    large_type2 = 4
    mini = 5


class GraspType(Enum):
    suction_and_finger = 1
    suction_only = 0
    finger_only = 2


class Item:
    def __init__(self, item_id, sku_no, dim1, dim2, dim3, weight, item_description):
        """Notes: dim1>dim2>dim3"""
        self.item_id = item_id
        self.sku_no = sku_no
        self.dim1 = dim1
        self.dim2 = dim2
        self.dim3 = dim3
        self.weight = weight
        self.item_description = item_description
        self.suctionCupConfig = set()
    
    def addSuctionCupConfig(self, suctionCupConfig):
        """scutionCupConfig should be a tuple with (SuctionCup, GraspType)"""
        self.suctionCupConfig.add(suctionCupConfig)
    
    def getSuctionCupConfig(self):
        return self.suctionCupConfig

    def __str__(self):
        pstr = ''
        for k, v in vars(self).items():
            pstr += f"{k}:{v};\n"
        return pstr


# Base Rule object. Every Rule object should provide the two method template
class BaseRule:
    def __init__(self):
        self.name = 'BaseRule'

    def isEligible(self, item: Item):
        '''returns a true/false(boolean) value for the selection logic to use.'''
        return False

    def getConfig(self):
        '''returns a tuple (suctionCupID, graspTypeID) for the selection logic to use.'''
        return SuctionCup.any, GraspType.suction_and_finger

############
#   MINI   #
############
# SuctionCup.large_type1


class MiniCupRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name = 'MiniCupRule'

    def isEligible(self, item: Item):
        return item.dim2 >= 0.18 and item.dim2 < 5 and item.weight < 0.8

    def getConfig(self):
        return SuctionCup.mini, GraspType.suction_and_finger


class MiniCupPreferred1SORule(MiniCupRule):
    '''Rule MiniCupPreferred1SO Implementation'''
    def __init__(self):
        super().__init__()
        self.name = 'MiniCupPreferred1SO'
    
    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim3 < 1.1 and item.dim1 < 5.8 and item.weight < 0.088
    
    def getConfig(self):
        return SuctionCup.mini, GraspType.suction_only


class MiniCupPreferred2(MiniCupRule):
    '''If the weight is <0.29 and max dim < 5.1, use mini'''

    def __init__(self):
        super().__init__()
        self.name = 'MiniCupPreferred2'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim3 < 0.29 and item.weight < 0.29

    def getConfig(self):
        return SuctionCup.mini, GraspType.suction_and_finger


############
#  Small   #
############
# SuctionCup.small


class SmallCupRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name = 'SmallCupRule'

    def isEligible(self, item: Item):
        return item.dim2 >= 0.25 and item.dim2 < 5 and item.weight < 0.8

    def getConfig(self):
        return SuctionCup.small, GraspType.suction_and_finger


class SmallCupPreferredCase3SO(SmallCupRule):
    def __init__(self):
        super().__init__()
        self.name = 'SmallCupPreferredCase3SO'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim3 < 1.1 and item.dim1 < 7.25 and item.weight < 0.11

    def getConfig(self):
        return SuctionCup.small, GraspType.suction_only


class SmallCupPreferredCase2(SmallCupRule):
    '''If the weight is <0.49 and max dim < 9.26'''
    def __init__(self):
        super().__init__()
        self.name = 'SmallCupPreferredCase2'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim1 < 9.26 and item.weight < 0.49

    def getConfig(self):
        return SuctionCup.small, GraspType.suction_and_finger


class SmallCupPreferredCase1(SmallCupRule):
    '''if weight is < 0.1 and min dimension is <med cup min med and and max dim < 6.5, use small'''
    def __init__(self):
        super().__init__()
        self.name = 'SmallCupPreferredCase1'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim1 < 6.5 and item.dim3 < 2 and item.weight < 0.1

    def getConfig(self):
        return SuctionCup.small, GraspType.suction_and_finger


############
#  Medium  #
############
#SuctionCup.medium


class MediumCupRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name = 'MediumCupRule'

    def isEligible(self, item: Item):
        return item.dim3 >= 2 and item.weight < 1.9

    def getConfig(self):
        return SuctionCup.medium, GraspType.suction_and_finger


############
#  large_type1   #
############
#SuctionCup.large_type1

class LargeT1CupRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name = 'LargeT1CupRule'

    def isEligible(self, item: Item):
        return item.dim3 >= 3 and item.weight < 6.6

    def getConfig(self):
        return SuctionCup.large_type1, GraspType.suction_and_finger


class LargeT1CupPreferredCase1(LargeT1CupRule):
    '''If the minimum dimension is bigger than the large_type1 Cup min med dim and weight > 0.40 (half smallest cup), use large_type1'''
    def __init__(self):
        super().__init__()
        self.name = 'LargeT1CupPreferredCase1'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.weight > 0.40

    def getConfig(self):
        return SuctionCup.large_type1, GraspType.suction_and_finger


class LargeT1CupPreferredCase2SO(LargeT1CupRule):
    '''If minimum dimension is < 1.1, and med dimension is > 4.95 then big cup and finger_only grasp, use large_type1 + finger_only'''
    def __init__(self):
        super().__init__()
        self.name = 'LargeT1CupPreferredCase2SO'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim3 < 1.1 and item.dim2 > 4.95

    def getConfig(self):
        return SuctionCup.large_type1, GraspType.finger_only


############
#  Bag     #
############
#SuctionCup.large_type2

class LargeT2CupRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name = 'LargeT2BaseRule'

    def isEligible(self, item: Item):
        return item.dim2 >= 1.9 and item.weight < 2.42

    def getConfig(self):
        return SuctionCup.large_type2, GraspType.suction_and_finger


class LargeT2CupPreferred2(LargeT2CupRule):
    '''If minimum dimension is < 1.1, and med dimension is > 4.95 and weight < 0.968, use bag cup and stailized grasp'''
    def __init__(self):
        super().__init__()
        self.name = 'LargeT2CupPreferred2'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim3 < 1.1 and item.dim2 > 4.95 and item.weight < 0.968

    def getConfig(self):
        return SuctionCup.large_type2, GraspType.finger_only


class LargeT2CupPreferred1(LargeT2CupRule):
    '''If med dim < 5 and max dim < 12 and weight < 1.815, use bag cup and suction_and_finger'''
    def __init__(self):
        super().__init__()
        self.name = 'LargeT2CupPreferred1'

    def isEligible(self, item: Item):
        return super().isEligible(item) and item.dim2 < 5 and item.dim3 < 12 and item.weight < 1.815

    def getConfig(self):
        return SuctionCup.large_type2, GraspType.suction_and_finger
