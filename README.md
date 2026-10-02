# Redpanda Connect Jev

Experimental community alpha v0.1.3 · MIT.

## Français

Un processeur RPC Redpanda Connect enrichit chaque objet JSON avec `jev.outcome`, `jev.choice`, la probabilité et la version de politique.

Installation :

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
umask 077
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Variables serveur : `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Le champ `text` est lu dans le message ; une erreur du modèle échoue le processeur pour utiliser la gestion des erreurs du pipeline. Le routage aval peut utiliser `jev.outcome`.

Le processeur rejette un message qui possède déjà un champ `jev`, afin de ne pas écraser des données existantes.

Le pipeline d’exemple envoie les décisions valides vers `stdout` et conserve les entrées en échec, sous leur forme brute, dans `failed-inputs.txt`. Le fichier est ignoré par Git ; `umask 077` limite son accès. Pour une source durable, remplacer cette sortie par une file de messages en échec adaptée.

## English

A Redpanda Connect RPC processor enriches each JSON object with `jev.outcome`, `jev.choice`, probability, and policy version.

Setup:

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
umask 077
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Server variables: `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Keep secrets outside the repository and user-visible configuration.

The `text` field is read from the message; a model failure fails the processor so the pipeline can handle it. Downstream routing can use `jev.outcome`.

The processor rejects a message that already has a `jev` field, so existing data is not overwritten.

The example pipeline sends valid decisions to `stdout` and preserves failed inputs as raw lines in `failed-inputs.txt`. Git ignores this file; `umask 077` restricts access to it. For a durable input, replace this output with a suitable dead-letter queue.

## Español

Un procesador RPC de Redpanda Connect añade a cada objeto JSON `jev.outcome`, `jev.choice`, la probabilidad y la versión de la política.

Instalación:

```sh
python3.12 -m venv .venv
.venv/bin/pip install redpanda-connect
umask 077
rpk connect run --rpc-plugins=plugin.yaml connect.yaml
```

Variables del servidor: `TYPESAFE_API_KEY, JEV_TEXT_FIELD (optional / facultatif / opcional; default: text)`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Se lee el campo `text` del mensaje; un fallo del modelo hace fallar el procesador para que el flujo gestione el error. El enrutamiento posterior puede usar `jev.outcome`.

El procesador rechaza un mensaje que ya tenga un campo `jev` para no sobrescribir datos existentes.

El flujo de ejemplo envía las decisiones válidas a `stdout` y conserva las entradas fallidas como líneas sin modificar en `failed-inputs.txt`. Git ignora este archivo; `umask 077` limita el acceso. Para una entrada duradera, sustituye esta salida por una cola de mensajes fallidos adecuada.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic responses and an actual Redpanda SDK Message. Redpanda Connect 4.112.0 processed one live Jev event and routed a failed input to the review file; no broker was exercised. Threshold `0.9` must be calibrated on labeled data. / Les tests utilisent des réponses synthétiques et un vrai Message du SDK Redpanda. Redpanda Connect 4.112.0 a traité un événement Jev réel et dirigé une entrée en échec vers le fichier de revue ; aucun broker n’a été testé. Le seuil `0.9` doit être calibré. / Las pruebas usan respuestas sintéticas y un Message real del SDK Redpanda. Redpanda Connect 4.112.0 procesó un evento Jev real y envió una entrada fallida al archivo de revisión; no se probó ningún broker. El umbral `0.9` debe calibrarse.

Host reference / Référence de l’hôte / Referencia del host: https://docs.redpanda.com/connect/plugins/about/

Redpanda Connect v4.56+ and Python 3.12+ are required for dynamic RPC plugins. / Redpanda Connect v4.56+ et Python 3.12+ sont requis. / Se requieren Redpanda Connect v4.56+ y Python 3.12+.
