from tinkoff.invest import Client, InstrumentIdType


# Преобразуем формат Money Value в float
def money_value(units: int, nano: int, quantity: int = None, float_nano: float = 0.000000001) -> float:
    return round(units + nano * float_nano, 2) if quantity is None else round((units + nano * float_nano) * quantity, 2)


# Формируем словарь активов
def tinkoff_portfolio(tinkoff_api_token: str) -> dict:
    # Словарь для формирования портфеля акций и облигаций
    asset_portfolio = {'energy': [],
                       'real_estate': [],
                       'telecom': [],
                       'materials': [],
                       'financial': [],
                       'industrials': [],
                       'health_care': [],
                       'utilities': [],
                       'consumer': [],
                       'it': []}

    with Client(tinkoff_api_token) as client:
        id_accounts = client.users.get_accounts().accounts[0].id  # id аккаунта
        portfolio = client.operations.get_portfolio(account_id=id_accounts)  # Полная информация о портфеле

        sum_share_all = money_value(portfolio.total_amount_shares.units, portfolio.total_amount_shares.nano)  # Сумма акций в портфеле
        sum_bond_all = money_value(portfolio.total_amount_bonds.units, portfolio.total_amount_bonds.nano)  # Сумма облигаций в портфеле
        sum_all = sum_share_all + sum_bond_all  # Сумма акций и облигаций в портфеле

        for portfolio_positions in portfolio.positions:
            if portfolio_positions.instrument_type == 'share':
                share = client.instruments.share_by(id=portfolio_positions.figi, id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI)  # Полная информация об акции в портфеле

                name_share = share.instrument.name  # Название акции
                sector_share = share.instrument.sector  # Сектор экономики акции
                sum_share = money_value(portfolio_positions.current_price.units, portfolio_positions.current_price.nano, portfolio_positions.quantity.units)  # Цена акции в портфеле
                percent = sum_share / sum_all  # Процент акции в портфеле

                asset_portfolio[sector_share].append({'instrument_type': 'share',
                                                      'name': name_share,
                                                      'sum': sum_share,
                                                      'percent': percent})
            elif portfolio_positions.instrument_type == 'bond':
                bond = client.instruments.bond_by(id=portfolio_positions.figi, id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI)  # Полная информация об облигации в портфеле

                name_bond = bond.instrument.name  # Название облигации
                sector_bond = bond.instrument.sector  # Название облигации
                sum_bond_body = money_value(portfolio_positions.current_price.units, portfolio_positions.current_price.nano, portfolio_positions.quantity.units)  # Цена облигации в портфеле
                sum_bond_nkd = money_value(portfolio_positions.current_nkd.units, portfolio_positions.current_nkd.nano, portfolio_positions.quantity.units)  # Цена НКД в портфеле
                sum_bond = round(sum_bond_body + sum_bond_nkd, 2)  # Цена облигации в портфеле с НКД
                percent = sum_bond / sum_all  # Процент облигации в портфеле

                asset_portfolio[sector_bond].append({'instrument_type': 'bond',
                                                     'name': name_bond,
                                                     'sum': sum_bond,
                                                     'percent': percent})

        # Вернуть отсортированный по сумме процентов словарь
        return dict((key, value) for key, value in sorted(asset_portfolio.items(), key=lambda item: sum([value['percent'] for value in item[1]]), reverse=True))
