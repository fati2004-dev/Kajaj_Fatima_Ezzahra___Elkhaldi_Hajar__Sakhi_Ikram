# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Repérer et prioriser les avis clients négatifs afin que l'équipe du site e-commerce puisse les examiner et traiter les problèmes signalés plus rapidement.

## Utilisateur final (obligatoire)

L'équipe du service client consulte une file d'avis triés par sentiment et priorité, puis décide elle-même des réponses et des actions à entreprendre.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) La tâche répétitive de classification peut être apprise à partir d'avis historiques étiquetés par des personnes, ou d'un échantillon annoté par l'équipe si ces étiquettes n'existent pas encore. (c) Le volume important d'avis rend un classifieur peu coûteux par avis préférable à un appel génératif ; (d) une erreur de tri reste rattrapable puisque l'équipe vérifie les avis avant d'agir.

## Données nécessaires et leur origine (obligatoire)

Des avis clients historiques provenant de la plateforme e-commerce, associés à une étiquette de sentiment (négatif ou non négatif) et, si possible, à une priorité validée par le service client, seront utilisés. Les identifiants, coordonnées et numéros de commande seront supprimés ou masqués avant l'entraînement et l'évaluation.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test représentatif tenu à l'écart de l'entraînement, le F1 macro devra atteindre au moins 0,85 et le rappel de la classe « négatif » au moins 0,90. Le seuil est accepté seulement si ces résultats sont mesurés sur des avis anonymisés et vérifiés par l'équipe.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif mal classé peut retarder le traitement d'un problème, tandis qu'un avis positif mal classé surcharge la file prioritaire. Un agent consulte les avis triés, peut corriger leur classe et leur priorité, et reste responsable de toute réponse ou décision destinée au client.

## Risques éthiques ou de confidentialité (obligatoire)

Les avis peuvent contenir des noms, coordonnées, numéros de commande ou propos sensibles : ils doivent être anonymisés, protégés contre les accès non autorisés et conservés uniquement le temps nécessaire. Il faut aussi surveiller les erreurs selon les langues et les formulations afin que certains groupes de clients ne soient pas systématiquement moins bien servis.

## Approche écartée et pourquoi (facultatif)

Les règles par mots-clés sont écartées comme approche principale, car elles repèrent mal l'ironie, les fautes et les formulations variées, même si elles peuvent servir de contrôle simple. Un modèle génératif par avis serait plus coûteux au grand volume et n'est pas nécessaire pour cette classification répétitive.

