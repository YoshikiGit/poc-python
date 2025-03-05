# 利率
INTEREST_RATE = 1.102
# 年間投資額
ANNUALLY_INVESTMENT_AMOUNT = 1200000
# 投資年数
NUM_INVESTMENT = 20
# 生涯成長投資枠（1,200万円）
lifetime_growth_frame = 12000000

def compound_interest(ANNUALLY_INVESTMENT_AMOUNT, NUM_INVESTMENT, annually_change_list, lifetime_growth_frame) -> float:
    if NUM_INVESTMENT == 0:
        return sum(annually_change_list)
    
    if lifetime_growth_frame < 0:
        annually_change_list.append(0)
    else:
        lifetime_growth_frame = lifetime_growth_frame - ANNUALLY_INVESTMENT_AMOUNT
        if lifetime_growth_frame <= 0:
            # 限度額を超えた場合、残枠の金額を追加
            annually_change_list.append(ANNUALLY_INVESTMENT_AMOUNT + lifetime_growth_frame)
        else:
            # 新たな投資額を追加
            annually_change_list.append(ANNUALLY_INVESTMENT_AMOUNT)

    # 既存の資金を複利で成長させる（リストの内容を更新）
    for i in range(len(annually_change_list)):
        annually_change_list[i] = annually_change_list[i] * INTEREST_RATE
        
    
    return compound_interest(ANNUALLY_INVESTMENT_AMOUNT, NUM_INVESTMENT - 1, annually_change_list, lifetime_growth_frame)

print(compound_interest(ANNUALLY_INVESTMENT_AMOUNT, NUM_INVESTMENT, [], lifetime_growth_frame))