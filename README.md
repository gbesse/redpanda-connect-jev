# Redpanda Connect Jev

Experimental community alpha v0.1.2 · MIT.

## Français

Un processeur RPC Redpanda Connect enrichit chaque objet JSON avec `jev.outcome`, `jev.choice`, la probabilité et la version de politique.

Installation :

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Variables serveur : `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Le champ `text` est lu dans le message ; une erreur du modèle échoue le processeur pour utiliser la gestion des erreurs du pipeline. Le routage aval peut utiliser `jev.outcome`.

Le processeur rejette un message qui possède déjà un champ `jev`, afin de ne pas écraser des données existantes.

Le pipeline d’exemple utilise `reject_errored` : un message sans décision Jev valide ne part pas vers `stdout`. Pour une source durable, configurer les rejets ou une file de messages en échec selon la source.

## English

A Redpanda Connect RPC processor enriches each JSON object with `jev.outcome`, `jev.choice`, probability, and policy version.

Setup:

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Server variables: `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Keep secrets outside the repository and user-visible configuration.

The `text` field is read from the message; a model failure fails the processor so the pipeline can handle it. Downstream routing can use `jev.outcome`.

The processor rejects a message that already has a `jev` field, so existing data is not overwritten.

The example pipeline uses `reject_errored`: a message without a valid Jev decision does not reach `stdout`. For a durable input, configure rejection or a dead-letter queue for that input.

## Español

Un procesador RPC de Redpanda Connect añade a cada objeto JSON `jev.outcome`, `jev.choice`, la probabilidad y la versión de la política.

Instalación:

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Variables del servidor: `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Se lee el campo `text` del mensaje; un fallo del modelo hace fallar el procesador para que el flujo gestione el error. El enrutamiento posterior puede usar `jev.outcome`.

El procesador rechaza un mensaje que ya tenga un campo `jev` para no sobrescribir datos existentes.

El flujo de ejemplo usa `reject_errored`: un mensaje sin decisión Jev válida no llega a `stdout`. Para una entrada duradera, configura el rechazo o una cola de mensajes fallidos según la fuente.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic responses and an actual Redpanda SDK Message. One live Jev request validated the pinned model and response shape; no Redpanda Connect server was exercised. Threshold `0.9` must be calibrated on labeled data. / Les tests utilisent des réponses synthétiques et un vrai Message du SDK Redpanda. Un appel Jev réel a validé le modèle et la réponse ; aucun serveur Redpanda Connect n’a été testé. Le seuil doit être calibré. / Las pruebas usan respuestas sintéticas y un Message real del SDK Redpanda. Una llamada real a Jev validó el modelo y la respuesta; no se probó un servidor Redpanda Connect. El umbral debe calibrarse.

Host reference / Référence de l’hôte / Referencia del host: https://docs.redpanda.com/connect/plugins/about/

Redpanda Connect v4.56+ and Python 3.12+ are required for dynamic RPC plugins. / Redpanda Connect v4.56+ et Python 3.12+ sont requis. / Se requieren Redpanda Connect v4.56+ y Python 3.12+.
