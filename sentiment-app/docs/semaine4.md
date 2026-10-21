# Semaine 4 : tests approfondis et qualité, notes du binôme

## 1. Couverture

- La couverture initiale de l'étape A n'a pas été mesurée avant les premières corrections.
- Après les tests d'intégration : **97,65 %** pour `api/` (85 statements, 2 manquants).
- Les lignes 83–85 de `api/main.py` sont le démarrage Uvicorn sous `if __name__ == "__main__"` ; les tests HTTP utilisent `TestClient` et n'exécutent pas ce point d'entrée de serveur.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Une chaîne composée d'espaces passait la validation Pydantic, puis était refusée par la prédiction avec une forme d'erreur différente. | `test_frontieres_du_contrat[texte-blanc]` et `test_propriete_texte_blanc` | `field_validator` applique `str.strip()` dans `PredictRequest`. |
| `ValueError` provenant du modèle était interprétée comme une erreur de saisie 422. | `test_panne_modele_repond_500_sans_detail_interne[exception1]` | Le schéma valide les entrées ; toute panne pendant la prédiction est journalisée et renvoie 500 sans détail interne. |
| Un modèle aux classes inconnues pouvait démarrer sans correspondance de labels. | `test_classes_inattendues_refusent_le_demarrage` | Les classes sont vérifiées au démarrage contre les deux classes attendues. |
| Le modèle prenait une décision même lorsque sa confiance était basse. | `tests/test_jeu_or.py` et `src/courbe_seuil.py` | À moins de 0,60, l'API renvoie `INDETERMINE`. |

## 3. Seuil d'abstention

Mesures sur le jeu de test de démonstration (58 avis) :

| Seuil | Réponses | Part répondue | Exactitude des réponses | Erreurs | Vers un humain |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0,50 | 58 | 100 % | 0,879 | 7 | 0 |
| 0,60 | 42 | 72 % | 0,952 | 2 | 16 |
| 0,70 | 37 | 64 % | 1,000 | 0 | 21 |

Le seuil retenu est **0,60** : sur ce jeu de test, il évite cinq erreurs par rapport à 0,50 et envoie 16 avis à un humain.

## 4. Jeu d'or

Sur les 38 avis réunis dans `data/jeu_or.csv`, `src/bilan_jeu_or.py` rapporte **12 réponses justes, 20 abstentions et 6 erreurs franches déclarées**. Les six erreurs conservées comme `xfail(strict=True)` sont des formulations que le modèle de démonstration classe avec une confiance supérieure au seuil malgré l'absence de termes discriminants dans ses données d'entraînement.

Les six erreurs connues sont conservées plutôt que de modifier les étiquettes pour faire correspondre artificiellement le compte de référence.

## 5. Outils statiques

- L'état initial de Ruff et mypy n'a pas été mesuré avant les corrections ; aucun chiffre initial n'est rapporté.
- Après correction : `ruff check .` et `mypy api` terminent sans erreur.
- Les tests statiques ont révélé des imports inutilisés, des appels `zip()` sans `strict=True` et des noms ambigus dans des fichiers existants ; ils ont été corrigés. Les tests de type confirment le contrat `Literal`/`TypedDict` de bout en bout.

## Vérification finale

`pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95` : **81 passed, 4 xfailed**, couverture totale de `api/` **97,65 %**. Les quatre `xfail` correspondent aux erreurs connues listées dans le jeu d'or.
