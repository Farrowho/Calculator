import mysql.connector


def ann_payment(credit_sum, stavka, credit_time):
    """Ф-ия расчета аннуитетных платежей"""
    print(f'''Сумма кредита: {credit_sum} руб. 
Ставка: {stavka}%
Срок: {credit_time} месяцев
Месяц | Ежемесячный платеж | Основной долг | Долг по процентам | Остаток основного долга''')

    month_proc_stav = stavka / 100 / 12
    monthly_payment = round((month_proc_stav * (1 + month_proc_stav) ** credit_time / (
            (1 + month_proc_stav) ** credit_time - 1)) * credit_sum, 2)
    ostatok = credit_sum

    for month in range(1, credit_time + 1):
        percent_dolg = round(ostatok * month_proc_stav, 2)
        main_dolg = round(monthly_payment - percent_dolg, 2)
        ostatok = round(ostatok - main_dolg, 2)
        if ostatok < 1:
            ostatok = 0
        print(f'{month} | {monthly_payment} | {main_dolg} | {percent_dolg} | {ostatok}')


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="saveme"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT sum_add, stavka, credit_time FROM credits")
select = mycursor.fetchall()

for data in select:
    ann_payment(data[0], data[1], data[2])
