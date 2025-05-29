totalPayment = 1657920 # 払込金額総額（円）
maxPaymentPeriod = 10 * 12 # 払込期間（月）
operationPeriod = 22 * 12 # 運用期間（月）
maturityAge = 22; # 満期年齢
monthlyPayment = totalPayment / maxPaymentPeriod # 月払い保険料
annualRate = 0.013 # 年利
tax = 0.20315 # 税率

def calculate(totalAssets, monthlyPayment, paymentPeriod):
    # 終了条件：運用期間を超えた場合
    if paymentPeriod >= operationPeriod:
        return totalAssets
    
    # 月利を計算（年利を12で割る）
    monthlyRate = annualRate / 12
    
    # 利息計算（税引き後）
    monthlyInterest = totalAssets * monthlyRate * (1 - tax)
    
    # 払込期間中は月払い保険料を追加
    if paymentPeriod < maxPaymentPeriod:
        totalAssets = totalAssets + monthlyInterest + monthlyPayment
    else:
        # 払込終了後は利息のみ
        totalAssets = totalAssets + monthlyInterest
    
    # 再帰呼び出しの結果を返す
    return calculate(totalAssets, monthlyPayment, paymentPeriod + 1)

# 満期受取額
print(calculate(0, monthlyPayment, 0))
