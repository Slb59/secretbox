# Cycle de vie d'un memo

 
## exemple de memo
planifié 23/06, 
réalisé: none , 
report: none, 
périodicité: quotidien

## actions

23/06 : le mémo est validé => memo(planifié: 24/06, réalisé: 23/06 , report: none)
24/06 : le mémo est reporté au 28/06 => mémo(planifié: 28/06, réalisé: 23/06 , report: 24/06)
28/06 : le memo est reporté au 30/06 => memo(planifié: 30/06, réalisé: 23/06 , report: 24/06)
30/06 : le mémo est validé => mémo(planifié: 31/06, rélisé: 30/06 , report: none)