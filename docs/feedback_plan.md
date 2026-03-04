# Estado actual y plan de mejora (feedback de patrones)

## Estado actual del repo

El proyecto ya cumple con una base jugable 1v1 en Pygame y ahora quedó organizado por módulos, lo que facilita defender patrones sin que se vean forzados:

- `src/core/assets.py`: `AssetManager` como **Singleton** con caché de imágenes.
- `src/core/services.py`: `GameServices` como **Facade** para servicios comunes.
- `src/core/factories.py`: `ModeFactory` como **Factory Method** para crear modos.
- `src/gameplay/commands.py`: jerarquía **Command** (`MoveCommand`, `AttackCommand`).
- `src/gameplay/controllers.py`: **Strategy** (`HumanController`, `AIController`).
- `src/gameplay/character.py`: **Decorator** (`DamageBoost`, `Shield`) sobre `Character`.
- `src/modes/fight_mode.py`: modo de pelea integrado con los patrones.

## Qué falta para que quede "defendible" en entrega

1. Extraer interfaz de audio/eventos al Facade (`GameServices`) aunque sea con implementación mínima.
2. Añadir un segundo modo simple (por ejemplo `TrainingMode`) para que la Factory demuestre escalabilidad.
3. Añadir documento UML parcial por patrón (6 mini diagramas).
4. Agregar pruebas unitarias ligeras para:
   - caché de `AssetManager`
   - selección de `ModeFactory`
   - salida de comandos en `HumanController/AIController`
   - composición de `Decorator`

## Roadmap sugerido (corto)

- Semana 1: pruebas unitarias + UML parcial.
- Semana 2: `TrainingMode` y audio mínimo en `GameServices`.
- Semana 3: pulir informe final (intención, problema, participantes, evidencia en código).

Con esto puedes defender claramente "2 creacionales, 2 estructurales, 2 comportamentales" sin sobreingeniería.
