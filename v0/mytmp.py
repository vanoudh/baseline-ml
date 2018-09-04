
args = dict([('pred_PassengerId', 'on'), ('pred_Survived', 'on'),
    ('pred_Pclass', 'on'), ('pred_Name', 'on'), ('pred_Sex', 'on'),
    ('pred_Age', 'on'), ('pred_SibSp', 'on'), ('pred_Parch', 'on'),
    ('pred_Ticket', 'on'), ('pred_Fare', 'on'), ('pred_Cabin', 'on'),
    ('pred_Embarked', 'on')])

args
for k, v in args.iteritems():
    print(k, v)
