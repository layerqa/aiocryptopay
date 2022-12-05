from typing import List, Union

from ..models.rates import ExchangeRate


def get_rate(source: str, target: str, rates: List[ExchangeRate]) -> ExchangeRate:
    """Get rate by source and target

    Args:
        source (str): _description_
        target (str): _description_
        rates (List[ExchangeRate]): _description_

    Returns:
        ExchangeRate: _description_
    """
    for rate in rates:
        if rate.source == source and rate.target == target:
            return rate


def get_rate_summ(summ: Union[int, float], rate: ExchangeRate) -> Union[int, float]:
    """Get rate summ

    Args:
        summ (Union[int, float]): _description_
        rate (ExchangeRate): _description_

    Returns:
        Union[int, float]: _description_
    """
    return summ / rate.rate
