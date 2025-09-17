# 年利
ANNUAL_INTEREST_RATE = 0.05
# 月利益
MONTHLY_INTEREST_RATE = ANNUAL_INTEREST_RATE / 12
# 月額投資額
MONTHLY_INVESTMENT_AMOUNT = 16000
# 投資年数
NUM_INVESTMENT = 30
# 投資月数
NUM_INVESTMENT_MONTHS = NUM_INVESTMENT * 12

def calculate(MONTHLY_INVESTMENT_AMOUNT, NUM_INVESTMENT_MONTHS, annually_change_list):
    if NUM_INVESTMENT_MONTHS == 0:
        return sum(annually_change_list)
    
    # 積み立てた分に利率計上
    for i in range(len(annually_change_list)):
        annually_change_list[i] = annually_change_list[i] * (1 + MONTHLY_INTEREST_RATE)
    
    # 月ごとの投資額を追加
    annually_change_list.append(MONTHLY_INVESTMENT_AMOUNT)

    return calculate(MONTHLY_INVESTMENT_AMOUNT, NUM_INVESTMENT_MONTHS - 1, annually_change_list)

print(calculate(MONTHLY_INVESTMENT_AMOUNT, NUM_INVESTMENT_MONTHS, []))