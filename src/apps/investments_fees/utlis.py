from decimal import Decimal
from typing import Tuple, Type
from enum import Enum
from django.conf import settings

class DiscountPercentage(Enum):
    FIRST = Decimal('0.002')
    HALF = Decimal('0.005')
    ALL = Decimal('0.01')

def yearly_fees_before(amount:Type[Decimal], fee_percentage_value:Type[Decimal], year:int=0) ->Tuple[Decimal,str]:
    if year < 0:
        raise ValueError('Year must be positive')
    elif year >= 0 and year <= 1:
        return (fee_percentage_value * amount) * settings.YEARS_UPFRONT, 'Before-04-2019 Fee for first year'
    else:
        return (fee_percentage_value * amount), f'Before-04-2019 for year {year}'


def yearly_fees_after(amount:Type[Decimal], fee_percentage_value:Type[Decimal], year:int=0) ->Tuple[Decimal,str]:
    description = f'After-04-2019 for year {year}'
    if year < 0:
        raise ValueError('Year must be positive')
    elif year >= 0 and year <= 1:
        return (fee_percentage_value * amount) * settings.YEARS_UPFRONT, 'After-04-2019 Fee for first year'
    elif year == 2:
        return (fee_percentage_value * amount), description
    elif year == 3:
        return (fee_percentage_value - DiscountPercentage.FIRST.value) * amount, description
    elif year == 4:
        return (fee_percentage_value - DiscountPercentage.HALF.value) * amount, description
    else:
        return (fee_percentage_value - DiscountPercentage.ALL.value) * amount, description

