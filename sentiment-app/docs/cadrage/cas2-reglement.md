# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Permettre aux élèves et aux membres du personnel de poser des questions sur le règlement intérieur et d'obtenir une réponse fondée sur les articles applicables.

## Utilisateur final (obligatoire)

Les élèves, leurs parents et les membres du personnel utilisent l'assistant pour retrouver rapidement une règle ; les questions ambiguës ou sensibles sont transmises à la vie scolaire.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) Les réponses doivent s'appuyer sur les articles du règlement et en citer les références pour être vérifiables. (a) Il n'est pas nécessaire de disposer d'un grand jeu de questions déjà étiquetées : le système retrouve les passages pertinents dans des documents existants ; en cas d'information absente ou ambiguë, il doit s'abstenir plutôt que d'inventer une règle.

## Données nécessaires et leur origine (obligatoire)

La version officielle et à jour du règlement intérieur, ainsi que les annexes validées par l'établissement, seront découpées en passages conservant leurs titres et numéros d'article. Un jeu de questions-réponses fictives ou rédigées avec la vie scolaire servira à tester la recherche, les réponses et les citations.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test d'au moins 50 questions validées par la vie scolaire, au moins 90 % des réponses devront être jugées correctes et directement étayées par le règlement ; 100 % devront citer un article pertinent ou s'abstenir clairement. Toute réponse sans source recevable est un échec.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse erronée peut induire un élève en erreur sur ses droits ou ses obligations ; chaque réponse affiche donc le passage source et sa référence, et l'assistant s'abstient si la source ne suffit pas. Les cas ambigus ou disciplinaires sont soumis à un membre de la vie scolaire, qui confirme la règle avant qu'elle soit présentée comme décision officielle.

## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler des informations personnelles sur des élèves, notamment des mineurs : le système doit limiter la collecte et la conservation des questions et ne pas les réutiliser pour entraîner un modèle. Seuls les documents officiels approuvés sont indexés, avec des accès et une journalisation limités conformément aux règles de l'établissement.

## Approche écartée et pourquoi (facultatif)

Un modèle génératif seul est écarté, car il pourrait produire une règle plausible mais absente du règlement et ne fournir aucune source fiable. Des règles métier seules ne couvriraient pas la variété des formulations naturelles des questions.

