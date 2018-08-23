from Option_Name_Changer import option_name_changer as op

test_example = ["PUT - QQQ 100 @ 168 EXP 06/15/2018",
"PUT - HD 100 @185 EXP 05/18/2018",
"CALL- CY 100 @ 17 EXP 06/15/2018",
"DJ EURO STOXX 50 AUG-18 3700C",
"DJ EURO STOXX 50 AUG 18 3600C",
"ERICSSON LM-B SHS JUL 18 60.000P",
"DEUTSCHE POST JUL 18 33P",
"DEUTSCHE POST JUL 18 31P",
"PUT - HD 100 @185 1/2 EXP 05/18/2018",
"PUT - QQQ 100 @ 06/18 EXP 100",
"PUT - QQQ 100 @ 6/18 EXP 100 1/2",
"100 @ QQQ 6/17 EXP P",
"100 @ 1/2 QQQ 2018/05/07 C",
"DEUTSCHE POST 02-Dec-2018 3600C",
"DEUTSCHE POST DEC-02-2018 3500 1/2 C"]

for i in test_example:
    print(i)
    print(op.to_option(i))
    print()

