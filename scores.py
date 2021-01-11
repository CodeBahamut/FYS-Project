from flask_table import Table, Col


class Results(Table):
    playernumber = Col('playernumber', show=False)
    name = Col('name')
    score = Col('score')
