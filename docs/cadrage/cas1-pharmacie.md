# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Signaler au pharmacien les ordonnances auxquelles il manque un champ obligatoire afin qu'il puisse les vérifier avant leur validation.

## Utilisateur final (obligatoire)

Le pharmacien d'officine consulte les alertes pendant la vérification de chaque ordonnance et décide de la suite à donner.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) Les champs requis sont définis par des règles métier et réglementaires explicites, qui doivent pouvoir être contrôlées et expliquées. (a) Il n'est pas nécessaire de disposer d'exemples étiquetés pour vérifier la présence de ces champs ; (d) une omission non détectée peut avoir des conséquences sur la prise en charge, donc l'outil signale un problème sans jamais valider l'ordonnance à la place du pharmacien.

## Données nécessaires et leur origine (obligatoire)

Une liste validée des champs requis et des cas particuliers sera établie à partir des textes applicables et des procédures de la pharmacie, puis vérifiée par un pharmacien. Pour le TP, les essais utiliseront uniquement des ordonnances fictives ou synthétiques, jamais de données de santé réelles.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test fictif annoté et vérifié par un pharmacien, le rappel des champs obligatoires manquants devra atteindre au moins 0,99 et la précision au moins 0,95. Toute règle devra aussi réussir les tests unitaires couvrant chaque champ et les principaux cas particuliers avant un essai en conditions réelles.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une omission manquée pourrait laisser passer une ordonnance incomplète ; une alerte erronée pourrait retarder inutilement sa délivrance. Dans tous les cas, le pharmacien examine l'ordonnance et confirme ou rejette l'alerte avant toute décision ou délivrance.

## Risques éthiques ou de confidentialité (obligatoire)

Les ordonnances contiennent des données personnelles et des informations de santé particulièrement sensibles : aucune ordonnance réelle ne sera utilisée dans le TP, et tout futur traitement devra respecter le cadre légal, limiter les accès et protéger les données. Le système ne doit ni prendre de décision médicale ni remplacer le jugement du pharmacien.

## Approche écartée et pourquoi (facultatif)

Le machine learning est écarté car la vérification porte sur des champs explicitement définis et ne nécessite pas d'apprendre à partir d'exemples étiquetés. Un modèle génératif serait moins vérifiable et pourrait inventer ou omettre des informations.

