# 利率
interest_rate = 1.102
# 年間投資額
annually_investment_amount = 400000
# 投資年数
num_investment = 20

def compound_interest(annually_investment_amount, num_investment, annually_change_list) -> float:
    if num_investment == 0:
        return sum(annually_change_list)
    
    # 新たな投資額を追加
    annually_change_list.append(annually_investment_amount)

    # 既存の資金を複利で成長させる（リストの内容を更新）
    for i in range(len(annually_change_list)):
        annually_change_list[i] = annually_change_list[i] * interest_rate
        
    
    return compound_interest(annually_investment_amount, num_investment - 1, annually_change_list)

print(compound_interest(annually_investment_amount, num_investment, []))